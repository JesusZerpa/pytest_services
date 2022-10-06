import pytest
import socketio
from socketio import ASGIApp
from socketio.asyncio_client import AsyncClient
from multiprocessing import  Process
import uvicorn
import pytest
LISTIN_IF="127.0.0.1"
PORT=8000
BASE_URL="http://localhost:8000"



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
def controller():
    from pytest_services import Controller

    return Controller()

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def service(client,controller):
    from quart import jsonify
    from pytest_services import Service


    return Service(client,
        name="Servicio 1",
        test=True,
        scope="debug",
        )


@pytest.fixture(scope="session")
def sio(service):
    import socketio
    sio = socketio.AsyncServer(async_mode='asgi',cors_allowed_origins='*')
    
    @sio.on("prueba")
    async def prueba(data):
        await service.check("checkpoint-1",lambda:data["validacion"]=="hola mundo")
    
    return sio

def run_server(app,sio):
    
    from asgi import  app
    app = socketio.ASGIApp(sio, app, static_files={
        '/': 'app.html',
    })

    uvicorn.run(app,host='127.0.0.1', port=8000)

@pytest.fixture(scope="session")
def server(app,sio):
    
    proc = Process(target=run_server, args=(app,sio), daemon=True)
    proc.start() 
    yield
    proc.kill() # Cleanup after test




@pytest.mark.asyncio
async def test_read_main(server,client,controller):
    controller.join(service)
    controller.run()
    await asyncio.sleep(5)

    client=AsyncClient()
    await client.connect(BASE_URL)
    await client.emit("escribir",{"mi2":"data"})
    await asyncio.sleep(5)

    raise

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



def build_steps(service,controller):
    controller.join(service)
    service.step("checkpoint-1")


def build_steps2(service,controller):
    controller.join(service)
    service.step("checkpoint-1")
    service.step("checkpoint-2")

def build_routes(app,service):
    from socketio.asyncio_client import AsyncClient

    from socketio import AsyncClient

    @app.route("/webhook",methods=["POST"])
    async def route():
        from quart import request,jsonify
        data=await request.json
        
        await service.check("checkpoint-1",
            lambda: data["enviando"]=="Mensaje de prueba")
        
        return jsonify({"success":True})


def build_routes2(app,service):
    from easy_validator import UtilValidator
    util_validator=UtilValidator()
    
    def validator(data):

        util_validator.validate(data)

    @app.route("/webhook",methods=["POST"])
    @service("/webhook",validator,"desde una ruta")
    async def route():
        from quart import request,jsonify
        data=await request.json
        
        await service.check("checkpoint-1",
            lambda: data["enviando"]=="Mensaje de prueba")
        
        return jsonify({"success":True})

    @sio.on("message")
    @service("mensaje",validator,"Por aqui pase desde un websocket",socketio=True)
    async def message(data):
        pass


@pytest.mark.asyncio
async def test_main(app,service,controller):

    build_steps(service,controller)
    build_routes(app,service)
    controller.run()

    await service.post("webhook",json={
        "enviando":"Mensaje de prueba2"
        })
    print(controller.report())
    assert controller.test()

@pytest.mark.asyncio
async def test_decorator(app,service,controller):

    build_steps2(service,controller)
    build_routes2(app,service)
    controller.run()

    await service.post("webhook",json={
        "enviando":"Mensaje de prueba2"
        })
    print(controller.report())
    assert controller.test()
    

    