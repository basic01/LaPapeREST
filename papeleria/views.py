from .models import Producto, Usuario, Direccion, Compra
from .serializer import ProductoSerializer, UsuarioSerializer, DireccionSerializer, CompraSerializer, UsuarioLoginSerializer
from rest_framework  import generics
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#imports para class UsuarioList Y UsuarioDetail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

#imports para Email
from django.core.mail import send_mail, EmailMessage



#Clases para vistas Productos
    #Método GET all
class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    #Método GET único
class ProductoDetail(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


#Clases para vistas Usuarios
class UsuarioList(APIView):
    #Metodo GET all
    def get(self, request, format=None):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
    #Metodo POST
    def post(self, request, format=None):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            #Validar si usuario por registrar ya existe en la base de datos
            existencia = Usuario.objects.filter(correo=serializer.validated_data['correo']).exists() 
            banderaExist = 0
        
            #Si existe regresar una bandera con valor de 1
            if existencia:
                banderaExist = 1

            #Si no existe regresar una bandera con valor de 0 y guardar el POST
            else:
                # serializer.save()
                message =  '<html><h2>La Pape</h2><p>Da click en este enlace para confirmar tu cuenta:</p><a href="https://basic01.github.io/basic01/confirmacion.html?u=3">Link confirmación</a></html>'
                emails = ('lapape.papelerias@gmail.com',)
                msg = EmailMessage('Confirmación cuenta: Bienvenido a La Pape..', message, settings.EMAIL_HOST_USER, to = emails)
                msg.content_subtype = 'html'
                msg.send()
            
                banderaExist = 0

            #Regresar valor banderaExist
            return Response(banderaExist, status=status.HTTP_201_CREATED)
        return Response(2, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #Método GET único
class UsuarioDetail(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


#Clase para vistas Usuario Loign
class UsuarioLogin(APIView):
    #Metodo GET all
    def get(self, request, format=None):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
    #Metodo POST
    def post(self, request, format=None):
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            #Validar si usuario por loguear ya existe en la base de datos
            existencia = Usuario.objects.filter(correo=serializer.validated_data['correo']).exists() 
            banderaExist = 0
        
            #Si existe regresar serializer con datos usuario
            if existencia:
                usuario = Usuario.objects.filter(correo=serializer.validated_data['correo'], contraseña=serializer.validated_data['contraseña'])
                if(usuario):
                    banderaExist = 1
                    usuario = Usuario.objects.get(correo=serializer.validated_data['correo'])
                    serializer = UsuarioSerializer(usuario)
                    return Response(serializer.data)
                else:
                    banderaExist = 2
                    return Response(banderaExist)

            #Si no existe regresar una bandera con valor de 0 
            else:
                banderaExist = 0
                return Response(banderaExist)

        return Response(3, status=status.HTTP_400_BAD_REQUEST)


#Clases para vistas Direcciones
    #Método GET all, POST
class DireccionList(generics.ListCreateAPIView):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

    #Método GET único
class DireccionDetail(generics.RetrieveAPIView):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer


#Clases para vistas Compras
    #Método GET all, POST
class CompraList(generics.ListCreateAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    #Método GET único, PUT
class CompraDetail(APIView):

    def get_object(self, pk):
        try:
            return Compra.objects.get(pk=pk)
        except Compra.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        compra = self.get_object(pk)
        serializer = CompraSerializer(compra)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        compra = self.get_object(pk)
        serializer = CompraSerializer(compra, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['status'] == 1:
                message =  '<html><h2>La Pape</h2><p>Gracias por realizar el pago, tu compra ha sido confirmada.</p></html>'
                usuario = Usuario.objects.get(id=serializer.validated_data['usuario'].id)
                emails = ('lapape.papelerias@gmail.com', usuario.correo)
                msg = EmailMessage('Confirmación pago: Ticket La Pape..', message, settings.EMAIL_HOST_USER, to = emails)
                msg.content_subtype = 'html'
                msg.send()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

