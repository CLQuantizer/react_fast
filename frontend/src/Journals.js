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
			const url = 'http://127.0.0.1:8000/users/journals/';
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
	
	const strin = "#### A demo of **react-markdown**\n react-markdown \
	is a markdown component for React. is ";
	return (
      <Box maxW='lg' textAlign="left" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <VStack spacing={8}>
          	<UnorderedList fontSize='3xl'>
          		{ListOfJournals.map((j)=>
          			<ListItem key={j['id']}>
          					<Text>{j['title']}</Text>
							  <Text fontSize='sm'><ReactMarkdown>{j['body']}</ReactMarkdown></Text>
							  <Text fontSize='sm'><ReactMarkdown>{strin}</ReactMarkdown></Text>
          			</ListItem>)}
  			</UnorderedList>
	        </VStack>
        </Grid>
      </Box>
		
	);	
}

export default Journals;