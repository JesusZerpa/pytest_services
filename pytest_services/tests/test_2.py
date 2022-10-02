import pytest

@pytest.fixture(scope="session")
def app():
    from easy_validator import UtilValidator
    from quart import Quart
    
    app=Quart(__name__)
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    
    yield app

    # clean up / reset resources here

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
@pytest.fixture(scope="session")
def controller(app):
    from pytest_services import Controller

    return Controller()


@pytest.fixture(scope="session")
def service(client):
    from quart import jsonify
    from pytest_services import Service

    return Service(client,
        name="Servicio 1",
        test=True,
        scope="debug",
        )

@pytest.fixture(scope="session")
def build_steps(service,controller):
    controller.join(service)
    service.step("checkpoint-1")


@pytest.fixture(scope="session")
def build_routes(app,service):

    @app.route("/webhook",methods=["POST"])
    async def route():
        from quart import request,jsonify
        data=await request.json
        
        service.check("checkpoint-1",
            data["enviando"]=="Mensaje de prueba")
        
        return jsonify({"success":True})

@pytest.mark.asyncio
async def test_main(service,controller):
    await service.post("webhook",json={
        "enviando":"Mensaje de prueba2"
        })
    controller.test()
    