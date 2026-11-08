$carpeta = "C:\Users\Andrux\Downloads\espagnol"
$listaOriginal = Join-Path $carpeta "listaOriginal_Correcta.txt"
$listaNueva = Join-Path $carpeta "listaDeNombresNuevos.txt"
$destino = Join-Path $carpeta "traducido"

# Leer las listas SIN modificar los nombres ni quitar espacios
$originales = @(Get-Content -LiteralPath $listaOriginal -Encoding UTF8)
$nuevos = @(Get-Content -LiteralPath $listaNueva -Encoding UTF8)

# Crear carpeta de destino
New-Item -ItemType Directory -Path $destino -Force | Out-Null

$errores = @()
$movidos = 0

$total = [Math]::Min($originales.Count, $nuevos.Count)

for ($i = 0; $i -lt $total; $i++) {

    $nombreOriginal = $originales[$i]
    $nombreNuevo = $nuevos[$i]

    try {
        # Ignorar líneas vacías sin detener el proceso
        if ([string]::IsNullOrWhiteSpace($nombreOriginal) -or
            [string]::IsNullOrWhiteSpace($nombreNuevo)) {
            throw "Nombre vacío"
        }

        # Agregar .png si el nombre nuevo no tiene extensión PNG
        if ([IO.Path]::GetExtension($nombreNuevo) -ne ".png") {
            $nombreNuevo += ".png"
        }

        $origen = Join-Path $carpeta $nombreOriginal
        $rutaDestino = Join-Path $destino $nombreNuevo

        # Si no existe el original, pasar al siguiente
        if (-not (Test-Path -LiteralPath $origen -PathType Leaf)) {
            throw "No se encontró el archivo original"
        }

        # No sobrescribir archivos existentes
        if (Test-Path -LiteralPath $rutaDestino) {
            throw "El nombre nuevo ya existe en destino"
        }

        # Mover y renombrar
        Move-Item -LiteralPath $origen `
                  -Destination $rutaDestino `
                  -ErrorAction Stop

        $movidos++
        Write-Host "OK: [$nombreOriginal] -> [$nombreNuevo]" `
            -ForegroundColor Green
    }
    catch {
        $errores += "Línea $($i + 1): [$nombreOriginal] -> [$nombreNuevo] : $($_.Exception.Message)"
        Write-Host "IGNORADO: [$nombreOriginal] - $($_.Exception.Message)" `
            -ForegroundColor Yellow
    }
}

# Avisar si las listas tienen distinta cantidad de líneas
if ($originales.Count -ne $nuevos.Count) {
    $errores += "Las listas tienen diferente cantidad de líneas: originales=$($originales.Count), nuevos=$($nuevos.Count)."
}

# Guardar registro de errores
$archivoErrores = Join-Path $carpeta "errores_traduccion.txt"

if ($errores.Count -gt 0) {
    $errores | Out-File -LiteralPath $archivoErrores -Encoding UTF8
} elseif (Test-Path -LiteralPath $archivoErrores) {
    Remove-Item -LiteralPath $archivoErrores
}

Write-Host "`n========== RESUMEN ==========" -ForegroundColor Cyan
Write-Host "Movidos correctamente: $movidos"
Write-Host "Errores o archivos ignorados: $($errores.Count)"
Write-Host "Destino: $destino"

if ($errores.Count -gt 0) {
    Write-Host "Registro de errores: $archivoErrores" -ForegroundColor Yellow
}