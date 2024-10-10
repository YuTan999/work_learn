def get_sid():
    mutation = '''
    mutation {
         login(
              passwd: "proav101",
              user: "admin"
            ) {
              errorType {
                code
                message
              }
              user
              sid
            }
        }
    '''
    return mutation


def update_input_selection(sid, inst, input):
    mutation = f'''
    mutation {{
         updateInputSelection(
            sid: {sid},
            inst: {inst},
            input: {input}
          ) {{
            errorType {{
              code
              message
            }}
            inputSelection {{
                    inputselectionPrimary
                    inputselectionSecondary
                    inputselectionSwitchOn
                    inputselectionRestoreOn
                    inputselectionSwitchOverInterval
                    inputSelectionActive
                    inputselectionHdcpRxCapability
                    inputselectionSeamlessSwitchingState
                    inputselectionInputEnable
            }}
          }}
        }}
    '''
    return mutation


def update_fan_speed(sid, input):
    mutation = f'''
    mutation {{
         updateFanSpeed(
            sid: "{sid}",
            inst: ".0",
            input: {input}
            ) {{
              errorType {{
                code
                message
              }}
            }}
        }}
    '''
    return mutation


# mutation{
#   updateFanSpeed(
#     sid:"beQenn77gZEzhMUJeSenWyhufq54yNsX",
#     inst:".0",
#     input:{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_AUTO}){
#     errorType{
#       code
#       message
#     }
#   }
# }



# const[updateIpmxInput] = useMutation(UPDATE_IPMX_INPUT);
# export
# const
# UPDATE_IPMX_INPUT = gql
# `
# mutation
# updateIpmxInput($sid: String!, $inst: String!, $input: IpmxInputInput!) {
#     updateIpmxInput(inst: $inst, sid: $sid, input: $input) {
#     errorType
# {
#     code
# message
# }
# }
# }
# `;
#
# const[updateVideoDecode] = useMutation(UPDATE_RX_VIDEO_DECODE);
# export
# const
# UPDATE_RX_VIDEO_DECODE = gql
# `
# mutation
# updateVideoDecode($inst: String!, $sid: String!, $input: VideoDecodeInput!) {
#     updateVideoDecode(inst: $inst, sid: $sid, input: $input) {
#     videoDecode
# {
#     videodecodeFormatMode
# videodecodeManualResolution
# videodecodeManualFrameRate
# videodecodeCodec
# videodecodeWidth
# videodecodeHeight
# videodecodeScanType
# videodecodeFrameRate
# videodecodeChromaFormat
# videodecodeColorDepth
# videodecodeStatus
# inst
# }
# errorType
# {
#     code
# message
# }
# }
# }
# `;
#
