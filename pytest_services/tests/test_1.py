from pytest_services import Controller
from pytest_services import Service
import pytest
"""
En este test estaremos probando la funcionalidad de chequeo de pasos
en multiples aplicativos, esto sirve cuando se trabaja en red donde 

A -> B : check (A in B)
B -> C : check (B in C)
C -> A : check (C in A)

"""



@pytest.fixture(scope="session")
def app():
    from easy_validator import UtilValidator
    from quart import request,jsonify
    from server import app
    
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
def app2(app):
    from easy_validator import UtilValidator
    from quart import request,jsonify

    
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here


    yield app

    # clean up / reset resources here

@pytest.fixture(scope="session")
def client2(app):
    return app.test_client()

@pytest.fixture(scope="session")
def app3():
    from easy_validator import UtilValidator
    from server.validators import horarios_validator
    from quart import request,jsonify
    from server import app
    
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here


    yield app

    # clean up / reset resources here

@pytest.fixture(scope="session")
def controller(app):
    return Controller()
@pytest.fixture(scope="session")
def client3(app):
    return app.test_client()

@pytest.fixture(scope="session")
def service(client):
    from quart import jsonify
    return Service(client,
        name="Servicio 1",
        test=True,
        scope="debug",
        )

@pytest.fixture(scope="session")
def service2(client2):
    return Service(client2,
        name="Servicio 2",
        test=True,
        scope="debug",
        )

@pytest.fixture(scope="session")
def service3(client3):
    return Service(client3,
        name="Servicio 2",
        test=True,
        scope="debug",
        )

 
@pytest.fixture(scope="session")
def build_services(service,service2,service3):
    
    

@pytest.mark.asyncio
async def test_1(app,app2,app3):
    from quart import jsonify

    @app3.route("/webhook/<param>")
    async def route(param):
        from quart import request
        #paso 3
        
        service3.check(
            "param=='app3'",
            param=="app3")

        assert param=="app3"
        
        service3.check(
            "data['step']==2",
            data["step"]==2)

        assert data["step"]==2

        return jsonify({})

    @app.route("/webhook/<param>")
    async def route(param):
        from quart import request
        #paso 1
        
        await service.check("Iniciando")

        service2.post("/webhook/app2",json={
            "step":1
            })
        return jsonify({})

    @app2.route("/webhook/<param>")
    async def route(param):
        from quart import request
        #paso 2
        data=await request.json

        service2.check(
            "param=='app2'",
            param=="app2")

        assert param=="app2"
        
        service2.check(
            "data['step']==1",
            data["step"]==1)

        assert data["step"]==1
    
        service3.post(f"/webhook/app3",json={
            "step":2
            })
        return jsonify({})

    controller.join(service2,service3)

    service3.step("Iniciando Rutinas")
    service2.step("Iniciando")
    service2.step("param=='app2'")
    service2.step("data['step']==1")
    service3.step("param=='app3'")
    service3.step("data['step']==2")

def test_routine(service,service2,service3):
    
    service3.check("Iniciando Rutinas")
    service.post("/webhook/app3",json={
        "step":1
        })
    
