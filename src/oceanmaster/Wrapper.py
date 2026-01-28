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
    Called once per tick by the engine.

    Returns:
        dict:
        {
            "spawn": { bot_id: spawn_payload },
            "actions": { bot_id: action_payload }
        }
    """
    if api.get_tick() == 0:
        _STATE.bot_strategies.clear()
        _STATE.spawn_policy = load_spawn_policy()

    spawns: dict[str, dict] = {}
    actions: dict[str, dict] = {}

    for spec in _STATE.spawn_policy(api):
        strategy_cls = spec["strategy"]

        if not issubclass(strategy_cls, BotController):
            raise TypeError(f"Invalid strategy class in spawn_policy: {strategy_cls}")

        base_abilities = list(strategy_cls.DEFAULT_ABILITIES)
        extra_abilities = spec.get("extra_abilities", [])

        final_abilities = list(dict.fromkeys(base_abilities + extra_abilities))

        bot_id, payload = spawn(abilities=final_abilities, location=spec["location"])

        spawns[str(bot_id)] = payload

        _STATE.bot_strategies[bot_id] = strategy_cls(None)

    # ==================== EXECUTION PHASE ====================
    alive_ids: set[int] = set()

    for bot in api.get_my_bots():
        alive_ids.add(bot.id)

        if bot.id not in _STATE.bot_strategies:
            raise RuntimeError(f"No strategy registered for bot id {bot.id}")

        ctx = BotContext(api, bot)
        _STATE.bot_strategies[bot.id].ctx = ctx

        action = _STATE.bot_strategies[bot.id].act()
        if action:
            actions[str(bot.id)] = action.to_dict()

    # ==================== CLEANUP PHASE ====================
    for bot_id in list(_STATE.bot_strategies.keys()):
        if bot_id not in alive_ids:
            del _STATE.bot_strategies[bot_id]

    return {
        "spawn": spawns,
        "actions": actions,
    }
