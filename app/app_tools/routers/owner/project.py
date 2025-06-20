from fastapi import APIRouter, Depends, HTTPException

project = APIRouter(responses={404: {"Description": "Page not found"}})


@project.post('/')
def new_project():
    pass
