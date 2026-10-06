import asyncio
import aiohttp
from db import DbSession, create_db, close_db, SwapiCharacters

BASE_URL = "https://swapi-node.vercel.app"

# async def get_characters(id:int):
#     client = aiohttp.ClientSession()
#     response = await client.get(f"{BASE_URL}/api/people/{id}/")
#     json_data = await response.json()
#     await client.close()
#     return json_data

async def get_all_characters_info():
    async with aiohttp.ClientSession() as client:
        results = []
        for page_num in range(1, 11):
            response = await client.get(f"{BASE_URL}/api/people?page={page_num}&limit=10")
            json_data = await response.json()
            results.extend(json_data["results"])
        return results

async def insert_to_db(data):
    async with DbSession() as session:
        for character in data:
            fields = character["fields"]

            obj = SwapiCharacters(
                id=int(fields["url"].rsplit("/", 1)[-1]),
                birth_year=fields["birth_year"],
                eye_color=fields["eye_color"],
                films=",".join(fields["films"]),
                gender=fields["gender"],
                hair_color=fields["hair_color"],
                height=fields["height"],
                homeworld=fields["homeworld"],
                mass=fields["mass"],
                name=fields["name"],
                skin_color=fields["skin_color"],
                starships=",".join(fields["starships"]),
                vehicles=",".join(fields["vehicles"]),
            )
            session.add(obj)
        await session.commit()



async def main():
    await create_db()
    result = await get_all_characters_info()
    print(len(result))
    await insert_to_db(result)
    await close_db()

if __name__ == "__main__":
    coro = main()
    asyncio.run(coro)