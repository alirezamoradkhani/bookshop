# # app/scripts/seed.py

# import asyncio
# from app.unit_of_work import UnitOfWork

# from app.scripts.seed_data.baseusers import seed_user
# from app.scripts.seed_data.books import seed_book
# from app.scripts.seed_data.edition import seed_editions


# async def run_seed():
#     async with UnitOfWork() as uow:
#         print("🌱 Seeding started...")

#         await seed_user(uow)
#         await seed_book(uow)
#         await seed_orders(uow)

#         await uow.commit()

#         print("✅ Seeding completed!")


# if __name__ == "__main__":
#     asyncio.run(run_seed())