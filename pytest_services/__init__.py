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
from uuid import uuid4
from typing import Union,Tuple,List
class DB:
	pass

dbs={}
class Step:
	def __init__(self,checkpoint,controller):
		self.checkpoint=checkpoint
		self.checked=False
		if not self.controller.group.multiple:
			self.controller.group.pool.append(self)

		

class Group:
	def __init__(self,thread):
		self.pool=[thread]
		self.multiple=False
	def valid(self):
		evaluation=[]
		for thread in self.pool:
			evaluation.append(thread.valid())
		print(evaluation,any(evaluation))
		raise
		return any(evaluation)


class Thread:
	def __init__(self):
		self.pool=[]
	def valid(self):
		for step in self.pool:
			print(">>>>> Step: ",step.name," ",step.checked)
			if not step.checked:
				return False
		return len(self.pool)>0

class Controller:
	"""docstring for Controller"""
	def __init__(self,port=None):
		global dbs
		self.id=uuid4()
		self.steps=[]
		dbs[self.id]=[Group(Thread())]
		dbs[self.id][-1].used=True
		self.services=[]
		self.port=port
		self.processes={}
		from quart import Quart
		app=Quart(__name__)
		self.server=app

		@app.route("/microservice/<name>",methods=["POST"])
		async def microservice(name):
			global dbs
			from quart import request
			data=await request.json

			for thread in controller.group.pool:
				breaked=True
				for k,step in enumerate(thread):
					if k>0:
						if thread[k-1].checked:
							if step.checkpoint==data["checkpoint"] and name==step.name:
								step.checked=True
								break
					else:
						if step.checkpoint==data["checkpoint"] and name==step.name:
							step.checked=True
							break
				else:
					breaked=False
					if step.checked:
						self.controller.group=dbs[self.id][-1]

				if breaked:
					break
		

			return True

	def verify_prod_db(self):
		"""
		Verifica posibles errores en la base de datos que puede surjir 
		a partir de la manipulacion manual de los datos o de la no validacion de datos
		"""
	def catch(self,app):
		"""
		Captura todos los errores que puedan surgir de la ejecucion del sistema para notificarlo
		o tratar de corregirlo
		"""

	def add_solver(self,exception,action):
		"""
		crea una lista de soluciones posibles a errores que puedan presentarse
		"""
	def apply_solution(self,n_solution):
		"""
		Ejecuta la accion asociada a la excepcion 
		"""
	@property
	def routes(self):
		"""
		[
		[server_1,server_2],
		[server_2,server_1]
		]
		el enterior debe ser verdadero
		"""
		if dbs[self.id][-1].used:
			group=Group()
			group.multiple=True
		else:
			group=dbs[self.id][-1]
			group.multiple=True
		dbs[self.id].append(group)

		def posibilities(self,*threads:Tuple[List[...,Step]]):
			global dbs
			
			for thread in threads:
				t=Thread()

				for step in thread:
					step.build=False
					t.pool.append(step)
				group.pool.append(t)
			group.used=True
			
		return posibilities


	def join(self,*services):
		names=[]
		print("EEEEEEEE")
		for elem in services:
			if elem.name in names:
				raise Exception("Nombre de servicio ya existe")
			names.append(elem)

		for elem in services:
			if elem not in self.services:
				elem.controller=self
				self.services.append(elem)


	def run(self):
		"""
		Utilizado para levantar un servidor HTTP real 
		necesario cuando los servidors son externos
		"""
		import shlex

		for service in self.services:
			if service.command:
				command=shlex.split(service.command)
				p=Popen(command)
				self.processes[service.name]=p
		if self.server:
			self.server.run(port=self.port,debug=True)
		else:
			self.client=self.server.test_client()
	def test(self):
		global dbs
		
		evaluation=[]
		for group in dbs[self.id]:
			if not group.valid():
				evaluation.append(False)
				break

		result=all(evaluation)
		
		if not result:
			
			for k,group in enumerate(dbs[self.id]):
				print("-----------------------------------------")
				print(f"section {k}:")
				
				for k2,thread in enumerate(group.pool):
					print(f"\tThread {k2}:")
					
					for k3,step in enumerate(thread.pool):
						
						print(f"\t\tStep {k}: name={step.name} checked={step.checked}")
		return result

		




class CheckException(Exception):
	pass
class Service:
	def __init__(self,app:Union["Quart","Flask",str],name:str,host:str=None,
			test:bool=False,command:str=None,scope:str="debug"):
		self.url=None
		self.name=name
		self.command=command
		if type(app)==str:
			#se pasa la url del controlador
			self.url=app
			if not host:
				raise Exception("Se necesita especificar host")

		else:
			self.app=app
	
	async def post(self,endpoint,json={},headers={}):
		return await self.app.post(endpoint,json=json,headers=headers)

	async def get(self,endpoint,headers={}):
		return await self.app.get(endpoint,headers=headers)

	async def put(self,endpoint,headers={}):
		return await self.app.put(endpoint,json=json,headers=headers)

	async def delete(self,endpoint):
		return await self.app.delete(endpoint,json=json,headers=headers)

	async def patch(self,endpoint):
		return await self.app.patch(endpoint,json=json,headers=headers)

	def step(self,checkpoint:str) -> Step:
		return Step(checkpoint,self.controller)

	def check(self,checkpoint,value):
		if value==False:
			raise CheckException(value)

		self.controller.post(f"/microservice/{self.name}",
			json={"checkpoint":checkpoint})