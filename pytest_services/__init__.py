"""
from pytest_services import Service,parallel,ready

flow1,flow2= parallel([
	   	service.step("1"),service.step("2")],
	   [service2.step("1"),service2.step("2")
	   ])

assert ready(flow1,flow2,timeout=10)


service=Service("https://localhost:5000",
	name="Proceso a testear",
	test=True,
	scope="debug",
	)

@service.action("/process/{parametro}/",scope="debug")
def proceso(parametro):
	'''
	Luego ejecutamos otro proceso
	'''
	a=4
	b=4

	service.export("a",a)
	service.export("b",a)
	service.check_assert(parametro==20) #devuelve verdadero o falso en la verificacion hecha
	service.check_assert(a==b)
	service.checkpoint("checkpoint1") #envia una bandera de que paso por alli 

@app.route("/prueba/<id>",methods=["POST", ])
def prueba(id):
	print("accesando al id: ",id)
	proceso(request.json["dato"])

#############

def test_service():
	from pytest_services import Controller
	controller=Controller(5000)

	controller.service("Proceso a testear")
	scope=controller.verify("/process/{parametro}")
	controller.check_assert(scope.parametro==20)

	
	#ejecucion
	controller.test("http://localhost:5001")
	controller.post("/prueba/<id>",json={
		"dato":20
	})


"""