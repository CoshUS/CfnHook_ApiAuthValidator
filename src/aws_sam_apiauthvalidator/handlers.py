import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    BaseHookHandlerRequest,
    HandlerErrorCode,
    Hook,
    HookInvocationPoint,
    OperationStatus,
    ProgressEvent,
    SessionProxy,
    exceptions,
)

from .models import HookHandlerRequest, TypeConfigurationModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "AWS::SAM::ApiAuthValidator"

hook = Hook(TYPE_NAME, TypeConfigurationModel)
test_entrypoint = hook.test_entrypoint


@hook.handler(HookInvocationPoint.CREATE_PRE_PROVISION)
def pre_create_handler(
        session: Optional[SessionProxy],
        request: HookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    target_model = request.hookContext.targetModel
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.FAILED
    )
    resource_properties = target_model.get("resourceProperties")

    if validate_auth(resource_properties):
        progress.status = OperationStatus.SUCCESS
    else:
        progress.status = OperationStatus.FAILED
        progress.message = "Not all paths and methods contain authorizer."
    return progress


@hook.handler(HookInvocationPoint.UPDATE_PRE_PROVISION)
def pre_update_handler(
        session: Optional[SessionProxy],
        request: BaseHookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    target_model = request.hookContext.targetModel
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.FAILED
    )
    resource_properties = target_model.get("resourceProperties")

    if validate_auth(resource_properties):
        progress.status = OperationStatus.SUCCESS
    else:
        progress.status = OperationStatus.FAILED
        progress.message = "Not all paths and methods contain authorizer."
    return progress

@hook.handler(HookInvocationPoint.DELETE_PRE_PROVISION)
def pre_delete_handler(
        session: Optional[SessionProxy],
        request: BaseHookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    return ProgressEvent(
        status=OperationStatus.SUCCESS
    )


def validate_auth(resource_properties):
    paths = resource_properties.get("Body", {}).get("paths")
    if not paths:
        return True
    for path, methods in paths.items():
        for method, method_definition in methods.items():
            security = method_definition.get("security", [])
            if not security:
                return False

    return True