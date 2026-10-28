*** Settings ***
Documentation     Herai Device Security Analysis CLI Integration Tests
Library           OperatingSystem
Library           Process

*** Variables ***
${PYTHON_BIN}     python3
${MAIN_SCRIPT}    ${CURDIR}/../main.py
${VALID_JSON}     ${CURDIR}/../data/devices.json
${VALID_EXCEL}    ${CURDIR}/../data/devices.xlsx

*** Test Cases ***
CLI Execution With Default JSON Data
    [Documentation]    Sistemin varsayılan JSON verisi ile 0 çıkış kodu dönerek başarılı çalıştığını doğrular.
    ${result}=    Run Process    ${PYTHON_BIN}    ${MAIN_SCRIPT}    ${VALID_JSON}
    Should Be Equal As Integers    ${result.rc}    0
    Should Contain    ${result.stdout}    HERAI STUDIOS - CİHAZ GÜVENLİK ANALİZ RAPORU

CLI Execution With Excel Data
    [Documentation]    Excel (.xlsx) girdi dosyasının otomatik dönüştürülüp işlendiğini doğrular.
    ${result}=    Run Process    ${PYTHON_BIN}    ${MAIN_SCRIPT}    ${VALID_EXCEL}
    Should Be Equal As Integers    ${result.rc}    0
    Should Contain    ${result.stdout}    Aktif Cihaz Sayısı

CLI Execution With Nonexistent File Should Fail
    [Documentation]    Olmayan dosya verildiğinde özel istisnanın yakalanıp 1 koduyla çıktığını doğrular.
    ${result}=    Run Process    ${PYTHON_BIN}    ${MAIN_SCRIPT}    non_existent_file.json
    Should Be Equal As Integers    ${result.rc}    1
    Should Contain    ${result.stderr}    Analiz Kritik Hatası