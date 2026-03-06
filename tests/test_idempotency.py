from tools.fakke_backend import FakeClinicBackend

def test_idempotency_returns_same_response():
    backend = FakeClinicBackend(default_doctor="Dr_MuhammadRaufxon")

    r1 = backend.create_booking(
        date="2026-03-06",
        time="10:00",
        service="Umumiy tekshiruv",
        name="Ali",
        phone="9989011112233",
        idem_key="call1:1:create_booking",
        doctor="Dr_MuhammadRaufxon"
    )

    r2 = backend.create_booking(
        date="2026-03-06",
        time="10:00",
        service="Umumiy tekshiruv",
        name="Ali",
        phone="9989011112233",
        idem_key="call1:1:create_booking",
        doctor="Dr_MuhammadRaufxon"
    )

    assert r1 == r2
    assert r1["ok"] is True
    