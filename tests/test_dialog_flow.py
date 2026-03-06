from core.dialog_manager.manager import DialogManager, DialogTurn
from tools.fake_backend import FakeClinicBackend

def test_booking_happy_path():
    tools = FakeClinicBackend(default_doctor="Dr_MuhammadRaufxon")
    dm = DialogManager(tools=tools, default_doctor="Dr_MuhammadRaufxon")

    call_id = "c1"

    # turn 0 Greeting
    r0 = dm.handle(DialogTurn(user_text="Assalom alaykum", call_id=call_id, turn_id=0))
    assert "Oq Tabassum" in r0.text

    # Turn 1 Booking intent
    r1 = dm.handle(DialogTurn(user_text="Men uchrashuv yaratmoqchiman", call_id=call_id, turn_id=1))
    assert "Qaysi xizmatni" in r1.text

    # Turn 2 Service
    r2 = dm.handle(DialogTurn(user_text="Konssultatsiya", call_id=call_id, turn_id=2))
    assert "Qaysi kunga" in r2.text

    # Turn 3 date
    r3 = dm.handle(DialogTurn(user_text="2026-03-06", call_id=call_id, turn_id=3))
    assert "Qaysi vaqtda" in r3.text

    # Turn 4 time
    r4 = dm.handle(DialogTurn(user_text="10:00", call_id=call_id, turn_id=4))
    assert "Tasdiqlaysizmi?" in r4.text

    # Turn 5 confirmation
    r5 = dm.handle(DialogTurn(user_text="Ha", call_id=call_id, turn_id=5))
    assert "Ismingiz va telefon raqamingizni ayting" in r5.text

    # Turn 6 name, phone => booking created 
    r6 = dm.handle(DialogTurn(user_text="John Doe, +998901112233", call_id=call_id, turn_id=6))
    assert "Muvaffaqiyatli yaratildi" in r6.text
    