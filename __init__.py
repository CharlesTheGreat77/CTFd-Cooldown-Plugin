from .cooldown import ChallengeCooldownPlugin

def load(app):
    plugin = ChallengeCooldownPlugin()
    plugin.init_app(app)