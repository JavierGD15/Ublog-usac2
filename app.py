from flask import Flask, render_template, jsonify, request, redirect, url_for
import json




#Variables

usuarios=[{"name":"William Corado","gender":"M","username":"admin","email":" admin@ipc1.com","password":"admin@ipc1"}]
publis= {"images":[
                            {
            "url": "https://www.hogarmania.com/archivos/201104/salud-gatos-xl-668x400x80xX.jpg",
            "date": "03/10/2021",
            "category": "cats",
            "likes": 0,
            "usuario": "JavierGD"


        }
        ],"videos":[
                        {
                    "url": "https://www.youtube.com/embed/pnBACXBfXVY",
                    "date": "10/10/2021",
                    "category": "cats",
                    "likes": 0,
                    "usuario": "JavierGD"


                }
        ]}
infousuario = []
topsvideos = []
topsimages = []
informacionpublis={"images":[],"videos":[]}



app = Flask(__name__)


#Login inicial
@app.route('/')
def index():
    
    return render_template('index.html')

#Publicaciones
@app.route('/inicio/new-post')
def post():
    
    return render_template('post.html')  

#Publicaciones-post
@app.route('/inicio/new-post/carga', methods=['POST'])
def post_agregar():
    
    
    enlace = request.form['enlace']
    categoria = request.form['categoria']
    #si request.form['imagen'] falla, no se agrega nada
    try:
        imagen = request.form['imagen']
    except:
        imagen = ""
    #si request.form['video'] falla, no se agrega nada
    try:
        video = request.form['video']
    except:
        video = ""


    
    
    

    import datetime
    fecha = datetime.datetime.now()
    fecha = fecha.strftime("%d/%m/%Y")
    likes = 0
    

    if imagen == "on" and video == "on":
        return render_template('advertenciapost.html')

    elif imagen == "on":
        dato = infousuario[0]
        publis["images"].append({"url": enlace, "date": fecha, "category": categoria, "likes": likes, "usuario": dato})
        get_user(dato)
        return redirect(url_for('pag_principal'))



    elif video == "on":
        
        dato = infousuario[0]
        publis["videos"].append({"url": enlace, "date": fecha, "category": categoria, "likes": likes, "usuario": dato})
        get_user(dato)
        return redirect(url_for('pag_principal'))


#Acerca-de
@app.route('/acerca_de')
def acerca_de():
    
    return render_template('acerca_de.html')        


#Mision-vision
@app.route('/mision-mision')
def mision():
    
    return render_template('mision.html')    

#contacto
@app.route('/contacto')
def contacto():
    
    return render_template('contacto.html')      


#creador
@app.route('/creador')
def creador():
    
    return render_template('creador.html')   

     


        

    
 


#Página de registro
@app.route('/registro')
def registro():
    
    return render_template('registro.html')

#Página de prueba
@app.route('/prueba')
def prueba():
    return render_template('prueba.html')
   


#Carga de registro
@app.route('/inicio1' , methods = ['POST'])
def inicio1():
    alternativa=False
    for i in usuarios:
        if i["username"] == request.form['user']:
            alternativa = True
            break
        else:
            alternativa= False
    
    if alternativa == False:
        #Toma los valores del formulario
        userU= request.form['user']
        nombreU= request.form['nombres']
        generoU= request.form['gen']
        correoU= request.form['correo']
        contraseñaU= request.form['contraseña']
        alternativa=False
        
        #Guarda los valores y los guarda en el array en la ultima posición
        usuarios.append({"name":nombreU,"gender":generoU,"username":userU,"email":correoU,"password":contraseñaU})
       
        #Retornamos la página principal
         
        return redirect(url_for('index'))
        
    
    else:
        return render_template('advertenciausuario.html')
        alternativa= False

#Eliminar usuarios
@app.route('/inicio/eliminar' , methods = ['POST','GET'] )
def eliminar():
        x=0
                
        for i in usuarios:
         if i["username"] == request.form['username']:
            usuarios.pop(x)
                      
            break
         else:
            x=x+1
        return redirect(url_for('admin'))

#Eliminar publicaciones-images
@app.route('/inicio/eliminar-publicaciones-images' , methods = ['POST','GET'] )
def eliminar_publi_images():
        x=0
                
        for i in publis['images']:
         if i["usuario"] == request.form['usuario'] and i["url"] == request.form['url'] and i["date"] == request.form['date']:
            publis['images'].pop(x)
            x=0          
            break
         else:
            x=x+1
        return redirect(url_for('admin'))          

#Eliminar publicaciones-videos
@app.route('/inicio/eliminar-publicaciones-videos' , methods = ['POST','GET'] )
def eliminar_publi_videos():
        x=0
                
        for i in publis['videos']:
         if i["usuario"] == request.form['usuario'] and i["url"] == request.form['url'] and i["date"] == request.form['date']:
            publis['videos'].pop(x)
            x=0         
            break
         else:
            x=x+1
        return redirect(url_for('admin'))         





#PDF
@app.route('/inicio/PDF-usuarios' )
def PDF1():
      
            
        return render_template("usuarios.html",usuario = usuarios)


#PDF
@app.route('/inicio/PDF-publicaciones' )
def PDF2():
      
            
        return render_template("publis.html",images=publis['images'],videos=publis['videos'])        





#Importar JSON-usuarios
@app.route('/inicio/JSON' , methods = ['POST','GET'] )
def JSON():
    f =  request.files['src-file1']
    data = json.load(f)
           
           
    for client in data:
        usuarios.append({"name":client['name'],"gender":client['gender'],"username": client['username'],"email": client['email'],"password":client['password']})

    return redirect(url_for('admin'))
        
#Importar JSON-publicaciones
@app.route('/inicio/JSON-usuarios' , methods = ['POST','GET'] )
def JSON_publis():
    f =  request.files['src-file1']
    data = json.load(f)
           
           
    for client in data['images']:
        publis['images'].append({"url":client['url'],"date":client['date'],"category": client['category'],"likes": 0,"usuario":""})

    for client in data['videos']:
        publis['videos'].append({"url":client['url'],"date":client['date'],"category": client['category'],"likes": 0,"usuario":""})    

    return redirect(url_for('admin'))




#Página editar usuarios
@app.route('/inicio/editar' , methods = ['POST'] )
def editar():
        
        

        userU= request.form['username']
        nombreU= request.form['name']
        generoU= request.form['gender']
        correoU= request.form['email']
        contraseñaU= request.form['password']
        
        return render_template('editar.html',userU=userU,nombreU=nombreU,generoU=generoU,correoU=correoU,contraseñaU=contraseñaU)


#Página editar publicaciones
@app.route('/inicio/editar-publicaciones' , methods = ['POST'] )
def editar_publi():
        
        
        tipo= request.form['tipo']
        url= request.form['url']
        date= request.form['date']
        category= request.form['category']
        likes=  request.form['likes']
        usuario= request.form['usuario']
        
        return render_template('editar_publi.html',tipo=tipo,url=url,date=date,category=category,usuario=usuario,likes=likes)        

#Carga de editar
@app.route('/inicio/editar/1' , methods = ['POST','GET'])
def editar1():
    alternativa=False
    for i in usuarios:
        if i["username"] == request.form['user']:
            i["username"]= request.form['user']
            i["name"]= request.form['nombres']
            i["gender"]= request.form['gen']
            i["email"]= request.form['correo']
            i["password"]= request.form['contraseña']
            alternativa = True
            
            break
        else:
            alternativa= False
    
    if alternativa == False:
        #Toma los valores del formulario
        userU= request.form['user']
        nombreU= request.form['nombres']
        generoU= request.form['gen']
        correoU= request.form['correo']
        contraseñaU= request.form['contraseña']
        alternativa=False
        
        #Guarda los valores y los guarda en el array en la ultima posición
        usuarios.append({"name":nombreU,"gender":generoU,"username":userU,"email":correoU,"password":contraseñaU})
       
        #Retornamos la página principal
        
        return redirect(url_for('admin'))
        alternativa= False
            
    else:
        return redirect(url_for('admin'))
        alternativa= False





#Carga de editar-publiaciones
@app.route('/inicio/editar/2' , methods = ['POST','GET'])
def editar2():
    alternativa=False

    if (request.form['tipo'] == "image"):   


        for i in publis['images']:
            if i["usuario"] == request.form['usuario'] and i["url"] == request.form['url'] and i["date"] == request.form['date']:

                i["url"]= request.form['url']
                i["date"]= request.form['date']
                i["category"]= request.form['category']
                i["likes"]= int(request.form['likes']) 
                i["usuario"]= request.form['usuario']
                alternativa = True
                
                break
            else:
                alternativa= False
        
        if alternativa == False:
            #Toma los valores del formulario
            tipo= request.form['tipo']
            url= request.form['url']
            date= request.form['date']
            category= request.form['category']
            likes= int(request.form['likes'])
            usuario= request.form['usuario']
            
            
            
            #Guarda los valores y los guarda en el array en la ultima posición
            publis['images'].append({"url":url,"date":date,"category":category,"likes":likes,"usuario":usuario})
        
            #Retornamos la página principal
            
            return redirect(url_for('admin'))
        

        
        else:
            return redirect(url_for('admin'))
        
    else:
        for i in publis['videos']:
            if i["usuario"] == request.form['usuario'] and i["url"] == request.form['url'] and i["date"] == request.form['date']:
                
                i["url"]= request.form['url']
                i["date"]= request.form['date']
                i["category"]= request.form['category']
                i["likes"]= int(request.form['likes'])
                i["usuario"]= request.form['usuario']
                alternativa = True
                
                break
            else:
                alternativa= False
        
        if alternativa == False:
            #Toma los valores del formulario
            tipo= request.form['tipo']
            url= request.form['url']
            date= request.form['date']
            category= request.form['category']
            likes= int(request.form['likes'])
            usuario= request.form['usuario']
            
            
            
            #Guarda los valores y los guarda en el array en la ultima posición
            publis['videos'].append({"url":url,"date":date,"category":category,"likes":likes,"usuario":usuario})
        
            #Retornamos la página principal
            
            return redirect(url_for('admin'))
        

        
        else:
            return redirect(url_for('admin'))


#likes
@app.route('/inicio/like' , methods = ['POST'] )
def like():
    if (request.form['tipo'] == "image"): 

        for i in publis['images']:    
            if i["usuario"] == request.form['usuario'] and i["url"] == request.form['url'] and i["date"] == request.form['date']:

                
                i["likes"]+= 1
                
                break
            else:
                 alternativa= False
                
        return redirect(url_for('pag_principal'))

    else:
        for i in publis['videos']:    
            if i["usuario"] == request.form['usuario'] and i["url"] == request.form['url'] and i["date"] == request.form['date']:
               
                i["likes"]+= 1
                
                
                break
            else:
                 alternativa= False
                
        return redirect(url_for('pag_principal'))


def get_user(username):

    informacionpublis["images"] =[]
    informacionpublis["videos"] =[]

    for i in publis['images']:
        if i["usuario"] == username:
            informacionpublis["images"].append(i)
            info = True

        else:
            info = False    

    if info == False:
        informacionpublis["images"] =[]

    for i in publis['videos']:
        if i["usuario"] == username:
            informacionpublis["videos"].append(i)
            info1 = True

        else:
            info1 = False   


    if info1 == False:
        informacionpublis["videos"] =[]         
            
    return 

#Página principal carga
@app.route('/carga' , methods = ['POST'] )
def usuario():
    #Toma los valores del login
    nombreU= request.form['user']
    contraseñaU= request.form['contraseña']
    
    
    alternativa1 = False
    alternativa=False
    
    
   
    for i in usuarios:
        if request.form['user'] == "admin" and request.form['contraseña'] == "admin@ipc1":
            
            alternativa1= True
            break
        elif i["username"] == request.form['user'] and i["password"] == request.form['contraseña']:
            get_user(i["username"])
            infousuario.append(i["username"])                     
            alternativa = True
            break
        else:
            alternativa= False
    if alternativa == True:
        
        return redirect(url_for('pag_principal'))
        
    elif alternativa1 == True:
         return redirect(url_for('admin'))

    else:
        return render_template('advertencialogin.html')
        alternativa= False

def post():

    #usuarios con mas publicaciones
 

    contador = 0        
    for i in usuarios:
        for j in publis['videos']:
            if i["username"] == j["usuario"]:
                contador+= 1
        topsvideos.append({"username":i["username"],"contador":contador})
        contador= 0

    topsvideos.sort(key=lambda x: x["contador"], reverse=True)

    contador = 0
    for i in usuarios:
        for j in publis['images']:
            if i["username"] == j["usuario"]:
                contador+= 1
        topsimages.append({"username":i["username"],"contador":contador})
        contador= 0

    topsimages.sort(key=lambda x: x["contador"], reverse=True)
    
    publis['images'].sort(key=lambda x: x['likes'], reverse=True)
    publis['videos'].sort(key=lambda x: x['likes'], reverse=True)

                


    


#reportes
@app.route('/admin/reportes')
def reportes():
    post()
    top1imagenes = publis['images'][0]
    top2imagenes = publis['images'][1]
    top3imagenes = publis['images'][2]
    top4imagenes = publis['images'][3]
    top5imagenes = publis['images'][4]
    top1videos = publis['videos'][0]
    top2videos = publis['videos'][1]
    top3videos = publis['videos'][2]
    top4videos = publis['videos'][3]
    top5videos = publis['videos'][4]

    topusuarios = topsimages[0]
    topusuarios1 = topsimages[1]
    topusuarios2 = topsimages[2]
    topusuarios3 = topsimages[3]
    topusuarios4 = topsimages[4]
    topusuariosvideos = topsvideos[0]
    topusuariosvideos1 = topsvideos[1]
    topusuariosvideos2 = topsvideos[2]
    topusuariosvideos3 = topsvideos[3]
    topusuariosvideos4 = topsvideos[4]

    return render_template('reportes.html',top1imagenes=top1imagenes,top2imagenes=top2imagenes,top3imagenes=top3imagenes,top4imagenes=top4imagenes,top5imagenes=top5imagenes,top1videos=top1videos,top2videos=top2videos,top3videos=top3videos,top4videos=top4videos,top5videos=top5videos,topusuarios=topusuarios,topusuarios1=topusuarios1,topusuarios2=topusuarios2,topusuarios3=topusuarios3,topusuarios4=topusuarios4,topusuariosvideos=topusuariosvideos,topusuariosvideos1=topusuariosvideos1,topusuariosvideos2=topusuariosvideos2,topusuariosvideos3=topusuariosvideos3,topusuariosvideos4=topusuariosvideos4)


   

#Página admin
@app.route('/admin' )
def admin():    
    return render_template('admin.html',usuario = usuarios, images=publis['images'],videos=publis['videos'])

def ordenar():
    publis['images'].sort(key=lambda x: x['likes'], reverse=True)
    publis['videos'].sort(key=lambda x: x['likes'], reverse=True)
    informacionpublis["images"].sort(key=lambda x: x['likes'], reverse=True)
    informacionpublis["videos"].sort(key=lambda x: x['likes'], reverse=True)

#Página principal
@app.route('/inicio' )
def pag_principal():
    #ordenar por likes
    ordenar()

    return render_template('inicio.html', images=publis['images'],videos=publis['videos'], usuarioimagen = informacionpublis['images'], usuariovideo = informacionpublis['videos'])

   
    

if __name__ == '__main__':
    app.run(port=5000, debug=False)



        
 