import httpx

async def get_cgpa_sgpa(enrollment, password):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "http://localhost:3001/get-cgpa",
                json={"enrollment": enrollment, "password": password}
            )
            res.raise_for_status()
            return res.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}
