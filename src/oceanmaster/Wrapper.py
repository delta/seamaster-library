"""
ENGINE WRAPPER

Handles:
- Bot ID allocation
- Strategy persistence
- Context rebinding
- Cleanup of dead bots
- Engine contract compliance
"""

from .API import GameAPI
from .BotContext import BotContext
from .Translate import spawn
from .controllers.BotBase import BotController
from .User import spawn_policy


BOT_STRATEGIES: dict[int, BotController] = {}


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

    spawns: dict[str, dict] = {}
    actions: dict[str, dict] = {}

    for spec in spawn_policy(api):
        strategy_cls = spec["strategy"]

        if not issubclass(strategy_cls, BotController):
            raise TypeError(
                f"Invalid strategy class in spawn_policy: {strategy_cls}"
            )

        base_abilities = list(strategy_cls.DEFAULT_ABILITIES)
        extra_abilities = spec.get("extra_abilities", [])

        final_abilities = list(dict.fromkeys(
            base_abilities + extra_abilities
        ))

        bot_id, payload = spawn(
            abilities=final_abilities,
            location=spec["location"]
        )

        spawns[str(bot_id)] = payload

        # create strategy instance (ctx bound in execution phase)
        BOT_STRATEGIES[bot_id] = strategy_cls(None)

    # ========================================================
    # EXECUTION PHASE
    # ========================================================
    alive_ids: set[int] = set()

    for bot in api.get_my_bots():
        alive_ids.add(bot.id)

        if bot.id not in BOT_STRATEGIES:
            # This should never happen unless the backend
            # introduces bots without frontend consent
            raise RuntimeError(
                f"No strategy registered for bot id {bot.id}"
            )

        ctx = BotContext(api, bot)

        # rebind context every tick
        BOT_STRATEGIES[bot.id].ctx = ctx

        action = BOT_STRATEGIES[bot.id].act()
        if action:
            actions[str(bot.id)] = action.to_dict()

    # ========================================================
    # CLEANUP PHASE
    # ========================================================
    for bot_id in list(BOT_STRATEGIES.keys()):
        if bot_id not in alive_ids:
            del BOT_STRATEGIES[bot_id]

    # ========================================================
    # FINAL RETURN
    # ========================================================
    return {
        "spawn": spawns,
        "actions": actions,
    }
