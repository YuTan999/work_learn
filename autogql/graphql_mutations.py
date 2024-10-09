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