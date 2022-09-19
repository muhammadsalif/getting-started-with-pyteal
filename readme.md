# Getting started with pyteal and algorand sandbox demo

## Setting up development environment and project

- Clone sandbox from https://github.com/algorand/sandbox

- Create project folder with same architecture

- Create virtual python env in project folder
```python3 -m venv venv```

- Activate that virtual environment
```source ./venv/bin/activate```

- Run requirements.txt for install all the dependencies in that virtual env
```pip3 install -r requirements.txt```

- Select interpreter in vscode for removing errors of import etc.
  + Interpreter path in vs-code command pallette ./project/venv/bin/python3.9

- Link your project folder with docker compose file by adding volumes key in that file.

- Make sure docker is running and go to sandbox directory and run docker container
```./sandbox up```

- In project folder virtual env terminal run to build contract files 
```sh ./build.sh contracts.contract```
  + That will create a build folder in project directory and after compilation of pyteal code to teal files

- Entering in sandbox in sandbox directory terminal :
```./sandbox enter algod```

- reate an app by the following command
```goal app create --creator ADDRESS_OF_GOAL_ACCOUNT --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices NUMBER_OF_GLOBAL_BYTE_SLICES_IN_CONTRACT --global-ints NUMBER_OF_GLOBAL_INTS_SLICES_IN_CONTRACT --local-byteslices NUMBER_OF_LOCAL_BYTE_SLICES_IN_CONTRACT --local-ints NUMBER_OF_LOCAL_INTS_SLICES_IN_CONTRACT```


#### After the successful creation of the project moving on to the interaction with application  

## Interaction with application 
- Calling application with arguments:
```goal app call --app-id YOUR_DEPLOYED_APPLICATION_ID --from U63LJDZW7FG3IARWZZFDSAHVVSZWW4YBPQI3M2ECWKELHJXCCK6ZF2ZMQU --app-arg "str:optIn" —foreign-asset 1```

- app info
```goal app info —-app-id YOUR_DEPLOYED_APPLICATION_ID```

- Reading app 
```goal app read —-global --app-id YOUR_DEPLOYED_APPLICATION_ID --guess-format```

- Optin
```goal app optin  --app-id uint```

- Update
```goal app update [flags]```

- Account info
```goal account info -a U63LJDZW7FG3IARWZZFDSAHVVSZWW4YBPQI3M2ECWKELHJXCCK6ZF2ZMQU```

