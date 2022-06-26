import React, {useEffect, useState} from 'react';
import {
  Box,
  Text,
  VStack,
  Grid,
  ListItem,
  UnorderedList,
} from '@chakra-ui/react';
import ReactMarkdown from 'react-markdown';

function Journals(journals){
	const [ListOfJournals,setListOfJournal] = useState([]);
   	
	async function getData(){
		try{
			// devlopment server
			const url = 'http://127.0.0.1:8000/users/journals/';
			// production server
			// const url = 'http://langedev.net:8000/users/journals/';
			const response = await fetch(url,{method:'GET'});
			const json = await response.json();

			console.log('the response for from API is:');
						console.log(json);
			    	setListOfJournal(json);
			}catch(error){console.error(error);}
		}

	useEffect(() => {
		getData();
 	 }, []);
	
	return (
      <Box maxW='lg' textAlign="left">
        <Grid minH="100vh" p={3}>
          <VStack spacing={8}>
          	<UnorderedList fontSize='sm'>
          		{ListOfJournals.map((j)=>
          			<ListItem key={j['id']}>
          					<Text fontSize='2xl' fontWeight='bold'>{j['title']}</Text>
								<ReactMarkdown>{j['body']}</ReactMarkdown>
          			</ListItem>)}
  			</UnorderedList>
	        </VStack>
        </Grid>
      </Box>
		
	);	
}

export default Journals;