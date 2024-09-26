import addContext from 'mochawesome/addContext.js'
import supertest from 'supertest'
import { config } from '../../config.js'
import { expect, assert } from 'chai'
import getNestedValue from 'get-nested-value'

export async function request(context, method, path, body = undefined, auth = true, asserts = {statusCode : 200},  host = undefined, customHeaders = undefined) {
    const requestST = host ? supertest(host) : supertest(config[global.env].host)

    const headers = customHeaders ? customHeaders : {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(auth && {'Authorization': `Bearer ${config[global.env].token}`})
    }

    let response = null
    let responseBody

    switch (method) {
        case 'GET':
            response = await requestST.get(path).set(headers)
            responseBody = response.body

            await validateStatusCode(response.statusCode, asserts.statusCode, context, method, path, headers, response)

            if (asserts.expectedFields) {
                await validateFieldsExists(responseBody, asserts.expectedFields, context, method, path, headers, response)
            }

            if (asserts.expectedValues) {
                await validateExpectedValues(responseBody, asserts.expectedValues, context, method, path, headers, response)
            }

            if (asserts.executionVariables) {
                await setExecutionVariables(responseBody, asserts.executionVariables)
            }

            break
        case 'POST':
            response = await requestST.post(path).send(body).set(headers)
            responseBody = response.body

            await validateStatusCode(response.statusCode, asserts.statusCode, context, method, path, headers, response, body)

            if (asserts.expectedFields) {
                await validateFieldsExists(responseBody, asserts.expectedFields, context, method, path, headers, response, body)
            }

            if (asserts.expectedValues) {
                await validateExpectedValues(responseBody, asserts.expectedValues, context, method, path, headers, response, body)
            }

            if (asserts.executionVariables) {
                await setExecutionVariables(responseBody, asserts.executionVariables)
            }
     
            break
        case 'PATCH':
            response = await requestST.patch(path).send(body).set(headers)
            responseBody = response.body

            await validateStatusCode(response.statusCode, asserts.statusCode, context, method, path, headers, response, body)

            if (asserts.expectedFields) {
                await validateFieldsExists(responseBody, asserts.expectedFields, context, method, path, headers, response, body)
            }

            if (asserts.expectedValues) {
                await validateExpectedValues(responseBody, asserts.expectedValues, context, method, path, headers, response, body)
            }

            if (asserts.executionVariables) {
                await setExecutionVariables(responseBody, asserts.executionVariables)
            }

            break
        case 'DELETE':
            response = await requestST.delete(path).send(body).set(headers)
            responseBody = response.body

            await validateStatusCode(response.statusCode, asserts.statusCode, context, method, path, headers, response, body)

            if (asserts.expectedFields) {
                await validateFieldsExists(responseBody, asserts.expectedFields, context, method, path, headers, response, body)
            }

            if (asserts.expectedValues) {
                await validateExpectedValues(responseBody, asserts.expectedValues, context, method, path, headers, response, body)
            }

            if (asserts.executionVariables) {
                await setExecutionVariables(responseBody, asserts.executionVariables)
            }

            break
        case 'PUT':
            response = await requestST.put(path).send(body).set(headers)
            responseBody = response.body

            await validateStatusCode(response.statusCode, asserts.statusCode, context, method, path, headers, response, body)

            if (asserts.expectedFields) {
                await validateFieldsExists(responseBody, asserts.expectedFields, context, method, path, headers, response, body)
            }

            if (asserts.expectedValues) {
                await validateExpectedValues(responseBody, asserts.expectedValues, context, method, path, headers, response, body)
            }

            if (asserts.executionVariables) {
                await setExecutionVariables(responseBody, asserts.executionVariables)
            }

            break
        default:
            console.log('not valid request method provided')
    }

    return response
}

async function validateStatusCode(actual, expected, context, method, path, headers, response, requestBody) {
    try {
        expect(actual).to.be.equal(expected)
    } catch(error) {
        addRequestInfoToReport(context, method, path, headers, response, requestBody)
        assert.fail(error.actual, error.expected, `Actual is ${error.actual}, but expected was ${error.expected}`)
    }
}

async function validateFieldsExists(body, fields, context, method, path, headers, response, requestBody) {
    fields.every(field => {
        try {
            expect(getNestedValue(field, body), `${field} present in body`).not.to.be.undefined
        } catch (error) {
            addRequestInfoToReport(context, method, path, headers, response, requestBody)
            assert.fail(error.actual, error.expected, `${field} field is not present in body`)
        }
    })
}

async function validateExpectedValues(body, fields, context, method, path, headers, response, requestBody) {
    fields.forEach(field => {
        try {
            expect(getNestedValue(field.path, body), `${field.path} not equal to ${field.value}`).to.be.equal(field.value)
        } catch (error) {
            addRequestInfoToReport(context, method, path, headers, response, requestBody)
            const actual = getNestedValue(field.path, body)
            assert.fail(actual, field.value, `${field.path} expected value is ${field.value}, but actual was ${actual}`)
        }
    })
}

async function setExecutionVariables(body, variables) {
    variables.forEach(variable => {
        global.executionVariables[variable.name] = getNestedValue(variable.path, body)
    })
}

function addRequestInfoToReport(context, method, path, headers, response, body) {
    addContext(context, `${method} ${path}`)
    addContext(context, {
        title: 'REQUEST HEADERS',
        value: headers
    })
    if (body) {
        addContext(context, {
            title: 'REQUEST BODY',
            value: body
        })
    }
    addContext(context, {
        title: 'RESPONSE HEADERS',
        value: response.headers
    })
    addContext(context, {
        title: 'RESPONSE BODY',
        value: response.body
    })
}