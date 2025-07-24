from flask import Blueprint

## Base
from app.controllers import base_controller
base_blueprint = Blueprint('base_blueprint', __name__)
base_blueprint.route('/', methods=['GET'])(base_controller.index)
# ------------------------------------------------------------------------------------------------------------------------------------ #

# ## Interview
from app.controllers import interview_controller
interview_blueprint = Blueprint('interview_blueprint', __name__)
interview_blueprint.route('/create', methods=['POST'])(interview_controller.create)
interview_blueprint.route('/search', methods=['POST'])(interview_controller.search)
interview_blueprint.route('/start', methods=['POST'])(interview_controller.start)
interview_blueprint.route('/audio', methods=['GET'])(interview_controller.audio)
# # ------------------------------------------------------------------------------------------------------------------------------------ #

# ## Candidate
from app.controllers import candidate_controller
candidate_blueprint = Blueprint('candidate_blueprint', __name__)
candidate_blueprint.route('/create', methods=['POST'])(candidate_controller.create)
candidate_blueprint.route('/search', methods=['POST'])(candidate_controller.search)
# # ------------------------------------------------------------------------------------------------------------------------------------ #

# ## Job
from app.controllers import job_controller
job_blueprint = Blueprint('job_blueprint', __name__)
job_blueprint.route('/create', methods=['POST'])(job_controller.create)
job_blueprint.route('/search', methods=['POST'])(job_controller.search)
job_blueprint.route('/<job_id>/update', methods=['POST'])(job_controller.update)
# # ------------------------------------------------------------------------------------------------------------------------------------ #

def initialize_routes(app):
    @app.before_request
    def before_request(): base_controller.before_request()
    @app.after_request
    def after_request(response): return base_controller.after_request(response)

    app.register_blueprint(base_blueprint)

    app.register_blueprint(interview_blueprint, url_prefix='/api/v1/interviews')
    app.register_blueprint(job_blueprint, url_prefix='/api/v1/jobs')
    app.register_blueprint(candidate_blueprint, url_prefix='/api/v1/candidates')