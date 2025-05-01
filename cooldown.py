from datetime import datetime, timedelta
from flask import request, jsonify
from CTFd.models import Teams, Solves
from CTFd.utils.user import get_current_team
from CTFd.utils.decorators import authed_only
from CTFd.api.v1.challenges import ChallengeAttempt
import secrets # better than rando lib..

# { team_id: { challenge_id: (expires_at, blocking_team_name) } }
blocklist = {}
minutes = 3 # minutes for blocked submission

class ChallengeCooldownPlugin:
    def init_app(self, app):
        self.app = app
        # you have to override the submission route for the custom message
        # -> or blocked team(s) will get a blank submission
        app.view_functions['api.challenges_challenge_attempt'] = self.override_challenge_attempt

        @app.after_request
        def handle_solve(response):
            if request.endpoint == 'api.challenges_challenge_attempt' and response.status_code == 200:
                data = response.get_json()
                if data and data.get('data', {}).get('status') == 'correct':
                    chal_id = request.get_json().get('challenge_id')
                    team = get_current_team()
                    if chal_id and team:
                        self.add_cooldown(chal_id, team)
            return response

    @authed_only
    def override_challenge_attempt(self):
        team = get_current_team()
        data = request.get_json()
        challenge_id = data.get("challenge_id")
        now = datetime.utcnow()

        # get blocklist for said challenge
        cooldown_info = blocklist.get(team.id, {}).get(challenge_id)
        if cooldown_info:
            expires_at, blocker_name = cooldown_info
            if now < expires_at:
                remaining = int((expires_at - now).total_seconds()) # get time to show the poor victim(s)
                return jsonify({
                    "success": True,
                    "data": {
                        "status": "incorrect", # used for red color...
                                               # if there's a custom color method..lmk
                        # custom message
                        "message": f"Submission for this challenge was blocked by the {blocker_name} Team. Try again in {remaining} seconds ;)"
                    }
                }), 200 # can't send 404s.. or message doesn't appear...
            else:
                # cooldown expired -> clean up
                del blocklist[team.id][challenge_id]

        # normal submission
        return ChallengeAttempt().post()

    def add_cooldown(self, challenge_id, solving_team):
        now = datetime.utcnow()
        expire_time = now + timedelta(minutes=minutes)

        # list of teams yet to solve said challenge that's not the "solver"
        unsolved_teams = Teams.query.filter(
            ~Teams.id.in_(
                Solves.query.filter_by(challenge_id=challenge_id).with_entities(Solves.team_id)
            ),
            Teams.id != solving_team.id
        ).with_entities(Teams.id).all()

        if unsolved_teams:
            random_team_id = secrets.choice(unsolved_teams)[0] # pick a random victim!
            blocklist.setdefault(random_team_id, {})[challenge_id] = (expire_time, solving_team.name)