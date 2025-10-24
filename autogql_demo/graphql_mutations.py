def get_sid():
    mutation = '''
    mutation {
         login(
              passwd: "",
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


def update_input_selection(sid, inputs):
    mutation = f'''
    mutation {{
         updateInputSelection(
            sid: {sid},
            inst: ".0",
            input: {inputs}
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


def update_ipmx_input(sid, inst, inputs):
    mutation = f'''
    mutation {{
         updateIpmxInput(
            sid: "{sid}",
            inst: "{inst}",
            input: {inputs}
          ) {{
            errorType {{
              code
              message
            }}
          }}
        }}
    '''
    return mutation


def update_fan_speed(sid, inputs):
    mutation = f'''
    mutation {{
         updateFanSpeed(
            sid: "{sid}",
            inst: ".0",
            input: {inputs}
            ) {{
              errorType {{
                code
                message
              }}
            }}
        }}
    '''
    return mutation
