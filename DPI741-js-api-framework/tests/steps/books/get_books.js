import { request } from '../../utils/requests.js'

export async function getBooks() {
    it('Retrieve list of all books', async function () {
        await request(this, 'GET', '/books', undefined, false, 
            {
                statusCode : 200,
                expectedFields: [
                    '0.id',
                    '7.id',
                ],
                expectedValues: [
                                    {path: '0.id', value: 1},
                                    // {path: '6.id', value: 7},
                                ]
            }
        )
    })
}