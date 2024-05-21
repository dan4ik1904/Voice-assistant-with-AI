const axios = require('axios');
const express = require('express')

const app = express()


app.listen(3000, () => {
    console.log('servre started on PORT 3000')
})

app.get('/', (req, res) => {
    const options = {
        method: 'POST',
        url: 'https://open-ai21.p.rapidapi.com/chatgpt',
        headers: {
            'content-type': 'application/json',
            'X-RapidAPI-Key': 'cd4c397b06msh8f50e22bb98cef3p1ac956jsn81e957948b0a',
            'X-RapidAPI-Host': 'open-ai21.p.rapidapi.com'
        },
        data: {
            messages: [
              {
                role: 'user',
                content: req.query.text
              }
            ],
            web_access: false
          }
        };
      
      try {
          axios.request(options)
          .then(response => {
            console.log(response.data)
            res.json(response.data)
          })
      } catch (error) {
          console.error(error);
      }

})
