"""test_security.py - Pruebas de seguridad para rate limiting y validación"""

from backend.rate_limiter import RateLimiter, TokenBucketLimiter
from backend.input_validator import InputValidator

def test_rate_limiter():
    """Prueba el RateLimiter"""
    print("\n" + "="*60)
    print("🧪 TEST: RateLimiter")
    print("="*60)
    
    limiter = RateLimiter(max_calls=3, window_seconds=5)
    
    # Primeras 3 llamadas deben ser permitidas
    for i in range(3):
        allowed = limiter.is_allowed("user1")
        print(f"  Llamada {i+1}: {'✓ Permitida' if allowed else '✗ Rechazada'}")
    
    # La 4ª debe ser rechazada
    allowed = limiter.is_allowed("user1")
    print(f"  Llamada 4: {'✓ Permitida' if allowed else '✗ Rechazada (esperado)'}")
    
    # Ver tiempo de espera
    wait_time = limiter.get_wait_time("user1")
    print(f"  Tiempo de espera: {wait_time:.1f}s")

def test_token_bucket():
    """Prueba el TokenBucketLimiter"""
    print("\n" + "="*60)
    print("🧪 TEST: TokenBucketLimiter")
    print("="*60)
    
    bucket = TokenBucketLimiter(capacity=5, refill_rate=1.0)
    
    # Consumir tokens
    for i in range(6):
        consumed = bucket.consume(1.0, "user1")
        available = bucket.get_available_tokens("user1")
        print(f"  Intento {i+1}: {'✓' if consumed else '✗'} - Disponibles: {available:.1f}")

def test_input_validator():
    """Prueba el InputValidator"""
    print("\n" + "="*60)
    print("🧪 TEST: InputValidator")
    print("="*60)
    
    validator = InputValidator()
    
    # Pruebas de filenames
    print("\n  📄 Validación de Filenames:")
    test_cases = [
        ("recording_123.mp3", True),
        ("../../../etc/passwd", False),
        ("file<script>.mp3", False),
        ("meeting 2025-02-11.wav", True),
        ("toolongnamethatwillexceedthemaximumlengthallowedforfilenamesinthesystemandshouldfailvalidation" * 5 + ".mp3", False),
    ]
    
    for filename, should_pass in test_cases:
        valid, error = validator.validate_filename(filename)
        status = "✓" if valid == should_pass else "✗"
        print(f"    {status} '{filename[:40]}...' -> {valid} ({error or 'OK'})")
    
    # Pruebas de keywords
    print("\n  🔑 Validación de Keywords:")
    test_cases = [
        ("oportunidad", True),
        ("cliente importante", True),
        ("a" * 150, False),  # Muy largo
        ("", False),  # Vacío
        ("normal keyword", True),
    ]
    
    for keyword, should_pass in test_cases:
        valid, error = validator.validate_keyword(keyword)
        status = "✓" if valid == should_pass else "✗"
        print(f"    {status} '{keyword[:30]}...' -> {valid} ({error or 'OK'})")
    
    # Pruebas de búsqueda
    print("\n  🔍 Validación de Búsqueda:")
    test_cases = [
        ("cliente", True),
        ("", True),  # Vacío es válido
        ("a" * 300, False),  # Muy largo
        ("búsqueda normal", True),
    ]
    
    for query, should_pass in test_cases:
        valid, error = validator.validate_search_query(query)
        status = "✓" if valid == should_pass else "✗"
        print(f"    {status} '{query[:30]}...' -> {valid} ({error or 'OK'})")
    
    # Pruebas de tamaño de audio
    print("\n  🎵 Validación de Tamaño de Audio:")
    test_cases = [
        (5 * 1024 * 1024, 100, True),      # 5MB < 100MB
        (150 * 1024 * 1024, 100, False),   # 150MB > 100MB
        (0, 100, False),                    # 0 bytes
    ]
    
    for size_bytes, max_mb, should_pass in test_cases:
        valid, error = validator.validate_audio_size(size_bytes, max_mb)
        status = "✓" if valid == should_pass else "✗"
        size_mb = size_bytes / (1024 * 1024)
        print(f"    {status} {size_mb:.1f}MB -> {valid} ({error or 'OK'})")

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("\n" + "🔐" * 30)
    print("     PRUEBAS DE SEGURIDAD")
    print("🔐" * 30)
    
    try:
        test_rate_limiter()
        test_token_bucket()
        test_input_validator()
        
        print("\n" + "="*60)
        print("✓ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60 + "\n")
    
    except Exception as e:
        print(f"\n✗ ERROR EN PRUEBAS: {e}\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
