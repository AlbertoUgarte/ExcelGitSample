*** Settings ***
Library                 QWeb
Library                 ExcelLibrary
Library                 String
Library                 ../libraries/GitOperations.py

*** Variables ***
${BROWSER}              chrome
${webshop}              https://qentinelqi.github.io/shop/
${excel_worksheet}      ${CURDIR}/../data/products_worksheet.xlsx
${git_branch}           main

*** Keywords ***
Setup Browser
    Open Browser        about:blank     ${BROWSER}
    Evaluate            random.seed()    random    # initialize random generator

End Suite
    Close All Browsers
