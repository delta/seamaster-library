"""
ENGINE wrapper module.
Handles:
- Bot ID allocation
- Strategy persistence
- Context rebinding
- Cleanup of dead bots
- Engine contract compliance
"""

import importlib
import sys
from oceanmaster.api import GameAPI
from oceanmaster.context.bot_context import BotContext
from oceanmaster.translate import spawn
from oceanmaster.botbase import BotController


class _EngineState:
    """
    Internal mutable engine state.
    """

    def __init__(self):
        self.bot_strategies: dict[int, BotController] = {}
        self.spawn_policy = None


_STATE = _EngineState()


def load_spawn_policy():
    """
    Load the spawn policy from user.py.
    """
    try:
        user = importlib.import_module("user")
    except ModuleNotFoundError as exc:
        raise RuntimeError("Submission must define user.py") from exc

    if not hasattr(user, "spawn_policy"):
        raise RuntimeError("user.py must define spawn_policy(api)")

    return user.spawn_policy


def play(api: GameAPI):
    """
    Main entrypoint called by the Python process for every tick.

    Engine invariants:
    - spawn_policy is executed ONLY at tick 0
    - Bot ID → Strategy mapping is created exactly once
    - Strategies persist across ticks
    - Cleanup must NOT run at tick 0
    """
    
    print(
        f"[ENGINE] tick={api.get_tick()} strategies={list(_STATE.bot_strategies.keys())}",
        file=sys.stderr,
    )

    # ---- LOAD SPAWN POLICY ONCE PER PROCESS ----
    if _STATE.spawn_policy is None:
        _STATE.bot_strategies.clear()
        _STATE.spawn_policy = load_spawn_policy()

    spawns: dict[str, dict] = {}
    actions: dict[str, dict] = {}

    # ---- SPAWN PHASE (ONLY AT TICK 0) ----
    if api.get_tick() == 0:
        for spec in _STATE.spawn_policy(api):
            strategy_cls = spec["strategy"]

            if not issubclass(strategy_cls, BotController):
                raise TypeError(
                    f"Invalid strategy class in spawn_policy: {strategy_cls}"
                )

            base_abilities = list(strategy_cls.DEFAULT_ABILITIES)
            extra_abilities = spec.get("extra_abilities", [])
            final_abilities = list(dict.fromkeys(base_abilities + extra_abilities))

            if(ctx.can_spawn(final_abilities) == False):
                print("[ENGINE] Cannot spawn bot due to insufficient resources.", file=sys.stderr)
                bot_id, payload = spawn(
                    abilities=final_abilities,
                    location=spec["location"],
                )

                spawns[str(bot_id)] = payload
                target = spec.get("target")

            if target is not None:
                _STATE.bot_strategies[int(bot_id)] = strategy_cls(None, target)
            else:
                _STATE.bot_strategies[int(bot_id)] = strategy_cls(None)


    # ---- ACTION PHASE ----
    alive_ids: set[int] = set()

    for bot in api.get_my_bots():
        alive_ids.add(bot.id)

        if bot.id not in _STATE.bot_strategies:
            raise RuntimeError(
                f"No strategy registered for bot id {bot.id}. "
                "Engine invariant violated: bot exists without strategy."
            )

        ctx = BotContext(api, bot)
        strategy = _STATE.bot_strategies[bot.id]
        strategy.ctx = ctx

        try:
            action = strategy.act()
        except Exception as exc:
            import traceback

            print(
                f"[ENGINE] Error in bot {bot.id}: {exc}\n{traceback.format_exc()}",
                file=sys.stderr,
            )
            action = None

        if action is not None:
            actions[str(bot.id)] = action.to_dict()

    # ---- CLEANUP PHASE (SKIP TICK 0) ----
    if api.get_tick() > 0:
        for bot_id in list(_STATE.bot_strategies.keys()):
            if bot_id not in alive_ids:
                del _STATE.bot_strategies[bot_id]

    return {
        "spawn": spawns,
        "actions": actions,
    }
