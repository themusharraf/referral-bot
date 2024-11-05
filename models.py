from tortoise import Tortoise, Model, fields
import uuid

class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(unique=True)
    referral_code = fields.CharField(max_length=36, unique=True)
    referred_by = fields.ForeignKeyField("models.User", related_name="referrals", null=True)
    referral_count = fields.IntField(default=0)  # Add this field to track referral count

    class Meta:
        table = "users"

    @classmethod
    async def generate_unique_referral_code(cls):
        while True:
            referral_code = str(uuid.uuid4())
            if not await cls.filter(referral_code=referral_code).exists():
                return referral_code



async def add_user(user_id: int, referred_by_code: str = None):
    referral_code = await User.generate_unique_referral_code()
    user = User(user_id=user_id, referral_code=referral_code, referred_by=None)

    if referred_by_code:
        referrer = await User.get_or_none(referral_code=referred_by_code)
        if referrer:
            user.referred_by = referrer
            referrer.referral_count += 1
            await referrer.save()

    await user.save()

async def startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()
