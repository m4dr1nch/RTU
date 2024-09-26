import { createUser } from '../../steps/customer/customer.js'
import { generateTestData } from '../../utils/helpers.js'

before(async () => {
    await generateTestData()
})

it('CRUD User', () => {
    describe(`CRUD User`, () => {
        createUser()
    })
})
