import pytest
import socketio,asyncio
from socketio import ASGIApp
from socketio.asyncio_client import AsyncClient
from multiprocessing import  Process
from pytest_services import Controller,Service
import uvicorn
import pytest
LISTIN_IF="127.0.0.1"
PORT=8000
BASE_URL="http://localhost:8000"

controller=Controller("127.0.0.1",8000)
service=Service(None,
        name="Servicio 1",
        test=True,
        scope="debug",
        )

@pytest.fixture(scope="session")
def app():
    
    from quart import Quart
    

    
    app=Quart(__name__)
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    
    yield app

    # clean up / reset resources her





@pytest.fixture(scope="session")
def client(app):
    return app.test_client()




@pytest.fixture(scope="session")
def sio():
    import socketio
    sio = socketio.AsyncServer(async_mode='asgi',cors_allowed_origins='*')
    
    @sio.on("prueba")
    async def message(data):
        await service.check("checkpoint-1",
            lambda:data["validacion"]=="Hola mundo")
    
    return sio

def build_steps(service,controller):

    controller.join(service)
    service.step("checkpoint-1")


def run_server(app,sio):
    build_steps(service,controller)

    app = socketio.ASGIApp(sio, app, static_files={
        '/': 'app.html',
    })

    uvicorn.run(app,host='127.0.0.1', port=8000)

@pytest.fixture(scope="session")
def server(app,sio):
    
    proc = Process(target=run_server, args=(app,sio), daemon=True)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaa")
    proc.start() 
    yield
    proc.kill() # Cleanup after test
@pytest.fixture(scope="session")
def controller_server():
    proc = Process(target=asyncio.run, args=(controller.run(),), daemon=True)
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbb")
    proc.start() 
    yield
    proc.kill() # Cleanup after test
    




@pytest.mark.asyncio
async def test_read_main(server,controller_server):


    await asyncio.sleep(5)

    client=AsyncClient()
    await client.connect(BASE_URL)
    await client.emit("escribir",{"validacion":"Hola mundo"})

    await asyncio.sleep(5)

    print(controller.report())
    assert controller.test()

"""
@pytest.fixture(scope="session")
def app():
    
    from quart import Quart
    
    app=Quart(__name__)
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    
    yield app

    # clean up / reset resources here
"""



