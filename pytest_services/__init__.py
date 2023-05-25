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
import requests
from uuid import uuid4
from typing import Union,Tuple,List
class DB:
    pass

dbs={}
class Step:
    def __init__(self,checkpoint,controller,service):
        self.checkpoint=checkpoint
        self.checked=False
        self.controller=controller
        self.service=service
        self.description=""

        if not self.controller.group.multiple:
    
            self.controller.group.pool[0].pool.append(self)
        


        

class Group:
    def __init__(self,thread):
        self.pool=[thread]
        self.multiple=False
    def valid(self):
        evaluation=[]
        for thread in self.pool:
            evaluation.append(thread.valid())
        
        return any(evaluation)


class Thread:
    def __init__(self):
        self.pool=[]
    def valid(self):
        for step in self.pool:
            if not step.checked:
                return False
        return len(self.pool)>0

class Controller:
    """docstring for Controller"""
    def __init__(self,host=None,port=None):
        global dbs
        self.id=uuid4()
        self.steps=[]
        dbs[self.id]=[Group(Thread())]
        self.group=dbs[self.id][-1]
        dbs[self.id][-1].used=True
        self.services=[]
        self.port=port
        self.host=host
        self.processes={}
        from quart import Quart
        app=Quart(__name__)
        self.app=app
        self.blocked=False#si un checkpoint se recibe mal colocado el controlador se bloqueara

        @app.route("/microservice/<name>",methods=["POST"])
        async def microservice(name):
            global dbs
            from quart import request
            data=await request.json
            valid=False
            if not self.blocked:
                for thread in self.group.pool:
                    breaked=True
                    for k,step in enumerate(thread.pool):
                        if k>0:
                            if thread[k-1].checked:
                                if step.checkpoint==data["checkpoint"] and name==step.service.name:
                                    step.checked=True
                                    valid=data["status"]
                                    step.description=data["description"]
                                    break
                            else:
                                break
                        else:
                        
                            if step.checkpoint==data["checkpoint"] and name==step.service.name:
                                valid=True
                                step.checked=data["status"]
                                step.description=data["description"]
                                break
                    else:
                        breaked=False
                        if step.checked:
                            self.controller.group=dbs[self.id][-1]

                    if breaked:
                        break
                self.blocked=not valid
                if self.blocked:
                    self.blocked_checkpoint=data["checkpoint"]
            return valid
    async def post(self,endpoint,json):
        if self.host:
            requests.post(self.host+endpoint,json=json)
        else:
            await self.client.post(endpoint,json=json)
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
    def report(self):
        report=""
        for k,group in enumerate(dbs[self.id]):
            report+="-------------------------------------------------\n"
            report+="REPORTE DE FLUJO DE OPERACION".center(50," ")+"\n"
            report+="-------------------------------------------------\n"
            if self.blocked:
                report+=("-----------------------------------------\n")
                report+=("Blockeo en checkpoint: "+self.blocked_checkpoint+"\n")
           
            report+=(f"Section {k+1}:\n")
            count=0
            for k2,thread in enumerate(group.pool):
                report+=(f"  Thread {k2+1}:\n")
                temporal=0
                for k3,step in enumerate(thread.pool):
                    separator="\t"+"..."*15
                    report+=(f"    Step {k3+1+count}: name={step.checkpoint} checked={step.checked}\n\tdescription:\n\n  {step.description}\n\n"+separator)
                    if step.checked: 
                        temporal+=k3
                    else:
                        temporal=0
                count+=temporal
        return report



    def join(self,*services):
        names=[]
        print("EEEEEEEE ",services)
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
        """
        import shlex

        for service in self.services:
            if service.command:
                command=shlex.split(service.command)
                p=Popen(command)
                self.processes[service.name]=p
        """
        if self.host:
            """
            self.thread=Thread(target=self.app.run,args=(self.host,self.port,False),daemon=True)
            self.thread.start()
            """
            print("jjjjjjjj")
        else:
            print("++++++++++++")
            self.client=self.app.test_client()
    def test(self):
        global dbs
        
        evaluation=[]
        for group in dbs[self.id]:
            if not group.valid():
                evaluation.append(False)
                break

        result=all(evaluation)
        
        if not result or self.blocked:
            report=self.report()
            raise Exception("\n"+report)
        return result

        




class CheckException(Exception):
    pass
class Service:
    def __init__(self,app:Union["Quart","Flask",str],name:str,host:str=None,
            test:bool=False,command:str=None,scope:str="debug"):
        self.url=None
        self.name=name
        self.host=host
        self.controller=None
        self.command=command
        if type(app)==str:
            #se pasa la url del controlador
            self.url=app
         

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
        return Step(checkpoint,self.controller,self)

    async def check(self,checkpoint,value,description=None):
        import inspect
        valid=False
        try:
            if callable(value):
                assert value()
            elif value==False:
                assert value
            valid=True
                
                
        except AssertionError:
            if callable(value):
                code=inspect.getsource(value).strip()
                line=inspect.getsourcelines(value)[1]
                _variables=""
                variables=dict(inspect.getclosurevars(value).nonlocals)
                variables.update(inspect.getclosurevars(value).globals)
                for elem in variables:
                    if type(variables[elem])!=str:
                        _variables+=elem+"="+str(variables[elem])+"\n"
                    else:
                        _variables+=elem+"='"+variables[elem]+"'\n"

                description="\n".join([
                f"\tAssertionError: {code} in {line}",
                f"\tvariables:\n\t\t{variables}"])
            else:
                description=f"""  AssertionError: 'False' for checkopint {checkpoint}"""

          
        if self.controller:

            await self.controller.post(f"/microservice/{self.name}",
                json={"checkpoint":checkpoint,"status":valid,"description":description})
        else:
            try:
                requests.post(self.host+f"/microservice/{self.name}",
                    json={"checkpoint":checkpoint,"status":valid,"description":description})
            except Exception as e:
                print(e)

        
    def __call__(self,checkpoint,validator_decorator=None,description="",socketio=False):
        """
        Decorador utilizado para rutas 
        """
        from functools import wraps
        def decorador2(fn):
           
            from my_validator import  ValidationError,ValidationRequired
            @wraps(fn)
            async def wrapper(*args,**kwargs):
              
                try:
                    async def testing(*args,**kwargs):
                        from quart import request
                        data=await request.json
                    value=await validator_decorator(testing)
                    await self.check(checkpoint,value,"Decorator success")
                   
                except ValidationError as e:
                  
                    await self.check(checkpoint,False,"ValidationError: "+str(e))
              
                except ValidationRequired as e:
                  
                    await self.check(checkpoint,False,"ValidationRequired: "+str(e))
                except Exception as e: 
                  
                    await self.check(checkpoint,False,"Exception: "+str(e))
                return await fn(*args,**kwargs)
            return wrapper


        return decorador2
