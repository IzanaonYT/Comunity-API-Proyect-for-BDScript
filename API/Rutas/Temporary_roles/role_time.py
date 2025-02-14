from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse
import requests
from API.Rutas.Temporary_roles.modelo import AddRole
from API.Funciones_API.convert_timestamp import segundos
import asyncio

router = APIRouter()



@router.post("/api/role_time/")
async def time_role(body: AddRole, token: str = Header(...), rol: str = Header(...)):
    add_role_url = f'https://discord.com/api/v9/guilds/{body.server}/members/{str(body.user)}/roles/{rol}'
    tiempo_segundos = segundos(body.tiempo)
    if tiempo_segundos == 0:
        raise HTTPException(detail="Error Time not 0 pls", status_code=399)
    
    
    headers_add_role = {
        'Authorization': f'Bot {token}'
    }
    
    
    response_add_role = requests.put(add_role_url, headers=headers_add_role)

    
    if response_add_role.status_code != 204:
        raise HTTPException(status_code=response_add_role.status_code, detail="Error adding role.")
    
    
    
    tiempo_segundos = segundos(body.tiempo)
    
    
    await asyncio.sleep(int(tiempo_segundos))
    
    
    remove_role_url = f'https://discord.com/api/v9/guilds/{body.server}/members/{str(body.user)}/roles/{rol}'
    
    
    headers_remove_role = {
        'Authorization': f'Bot {token}'
    }
    
    
    response_remove_role = requests.delete(remove_role_url, headers=headers_remove_role)
    
    
    if response_remove_role.status_code != 204:
        raise HTTPException(status_code=response_remove_role.status_code, detail="Error removing role.")
    
    
    return JSONResponse(content={"status": 200, "data": {"message": f"The role was successfully added to the user {body.user} and removed after {body.tiempo} seconds."}})