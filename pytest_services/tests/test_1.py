from pytest_services import Controller
from pytest_services import Service



@pytest.fixture(scope="session")
def app():
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
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def app2():
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
def client3(app):
    return app.test_client()

@pytest.fixture(scope="session")
def service(client):
    from quart import jsonify
    return service=Service(client,
        name="Servicio 1",
        test=True,
        scope="debug",
        )

@pytest.fixture(scope="session")
def service2(client2):
    return service2=Service(client2,
        name="Servicio 2",
        test=True,
        scope="debug",
        )

@pytest.fixture(scope="session")
def service3(client3):
    return service3=Service(client3,
        name="Servicio 2",
        test=True,
        scope="debug",
        )

 
@pytest.fixture(scope="session")
def build_services(service,service2,service3):
    
    service.join(service2,service3)

    service3.step("Iniciando Rutinas")
    service2.step("Iniciando")
    service2.step("param=='app2'")
    service2.step("data['step']==1")
    service3.step("param=='app3'")
    service3.step("data['step']==2")

@pytest.fixture(scope="session")
def create_routes(app,app2,app3):
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
        
        service.check("Iniciando")

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

def test_routine(service,service2,service3):
    
    service3.check("Iniciando Rutinas")
    service.post("/webhook/app3",json={
        "step":1
        })
    
