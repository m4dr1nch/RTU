import { getGreetings } from '../../steps/greetings/get_greetings.js'
import { generateTestData } from '../../utils/helpers.js'

before(async () => {
    await generateTestData()
})

it('Fetch greeting', () => {
    describe(`Fetch greeting`, () => {
        getGreetings()
    })
})
