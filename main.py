import GetUsersList
import CreateRegister

lista_usuarios = GetUsersList.main()

print(f'Cantidad de usuarios: {len(lista_usuarios)}')

print(lista_usuarios)

CreateRegister.main(lista_usuarios)

