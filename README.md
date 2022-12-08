# Clean Chat
## !! Warning
It's only a concept with a lot of additional work to be done

## How to run
Before all you need to create .env files for in clean-chat-back and clean-chat-front 
apps (you can just copy .env.template file for dev purposes).

You have to install docker and docker-compose on your machine,
then type following command:

```docker-compose -f docker-compose.dev.yml build``` - Only the first time

```docker-compose -f docker-compose.dev.yml up```

After that, the app should be running [here](http://localhost:5173)

## TODO
- Add channels feature
- Separate ml to different service
- Improve performance on the front end
- Replace sqlalchemy with better async orm
- Refactor code
