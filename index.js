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
      'X-RapidAPI-Key': '43631ce4f1msh20404de13215b39p1dc626jsn3ef12746d123',
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
