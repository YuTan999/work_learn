import requests
def get_device_info(sid):
   query = f"""
    query{{
      common{{
        getNmos(sid:"{sid}"){{
          nmos{{
            nmosName
          }}
        }}   
      }}
      system{{
        getImageUpdate(sid:"{sid}"){{
          imageUpdate{{
            updateCurrentVersion
          }}
        }}
      }}
    }}
   """
   return query


if __name__ == '__main__':
    sid = get_device_info("IKFHtb5kaX9C48uetqGDeYHMH0aU6thM")
    print(sid)
    response = requests.post('http://10.200.1.33/graphql', json={'query': sid}).json()
    print(response['data']['login']['sid'])