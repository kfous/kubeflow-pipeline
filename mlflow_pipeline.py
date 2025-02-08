from kfp import dsl
from kfp.components import create_component_from_func

def mlflow_logging():
    import subprocess
    # Dynamically install MLflow
    subprocess.run(["pip", "install", "--no-cache-dir", "mlflow"])

    import mlflow
    mlflow.set_tracking_uri("http://host.docker.internal:5000")
    mlflow.start_run()
    mlflow.log_param("param", 42)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.end_run()

mlflow_logging_op = create_component_from_func(
    mlflow_logging,
    base_image='python:3.8-slim'  # base Docker image with Python installed
)

@dsl.pipeline(
    name='MLflow Logging Pipeline',
    description='A pipeline that logs parameters and metrics to MLflow'
)
def mlflow_pipeline():
    mlflow_logging_op()

if __name__ == '__main__':
    from kfp.compiler import Compiler
    Compiler().compile(
        pipeline_func=mlflow_pipeline,
        package_path='mlflow_pipeline.yaml'
    )
