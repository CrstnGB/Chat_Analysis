import GetUsersList
import CreateRegister

lista_usuarios = GetUsersList.main()

print("hola git")

print(f'Cantidad de usuarios: {len(lista_usuarios)}')

print(lista_usuarios)

CreateRegister.main(lista_usuarios)

