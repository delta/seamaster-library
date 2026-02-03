"""
ENGINE wrapper module.
"""

import importlib
import sys
from oceanmaster.api import GameAPI
from oceanmaster.context.bot_context import BotContext
from oceanmaster.botbase import BotController
from oceanmaster.constants import Ability


class _EngineState:
    def __init__(self):
        self.bot_strategies: dict[int, BotController] = {}
        self.spawn_policy = None


_STATE = _EngineState()


def load_spawn_policy():
    try:
        user = importlib.import_module("user")
    except ModuleNotFoundError as exc:
        raise RuntimeError("Submission must define user.py") from exc

    if not hasattr(user, "spawn_policy"):
        raise RuntimeError("user.py must define spawn_policy(api)")

    return user.spawn_policy


def play(api: GameAPI):
    print(
        f"[ENGINE] tick={api.get_tick()} active={list(_STATE.bot_strategies.keys())}",
        file=sys.stderr,
    )

    # ---- LOAD SPAWN POLICY ONCE ----
    if _STATE.spawn_policy is None:
        _STATE.spawn_policy = load_spawn_policy()

    spawns: dict[str, dict] = {}
    actions: dict[str, dict] = {}

    # ---- SPAWN PHASE (EVERY TICK) ----
    for spec in _STATE.spawn_policy(api):
        strategy_cls = spec["strategy"]

        if not issubclass(strategy_cls, BotController):
            raise TypeError(
                f"Invalid strategy class in spawn_policy: {strategy_cls}"
            )

        abilities: list[Ability] = list(strategy_cls.ABILITIES)
        abilities += spec.get("extra_abilities", [])
        abilities = list(dict.fromkeys(abilities))

        if api.view.bot_count >= api.view.max_bots:
            continue

        bot_id = str(len(spawns))

        spawns[bot_id] = {
            "Ability": [a.value for a in abilities],
            "location": {"x": spec["location"], "y": 0},
        }
        _STATE.bot_strategies[int(bot_id)] = strategy_cls(None)

    # ---- ACTION PHASE ----
    alive_ids: set[int] = set()

    for bot in api.get_my_bots():
        alive_ids.add(bot.id)

        strategy = _STATE.bot_strategies.get(bot.id)
        if strategy is None:
            raise RuntimeError(
                f"Bot {bot.id} exists without a registered strategy."
            )

        ctx = BotContext(api, bot)
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

    # ---- CLEANUP PHASE ----
    for bot_id in list(_STATE.bot_strategies.keys()):
        if bot_id not in alive_ids:
            del _STATE.bot_strategies[bot_id]

    return {
        "spawn": spawns,
        "actions": actions,
    }
