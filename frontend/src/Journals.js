import React, {useEffect, useState} from 'react';
import {
  ChakraProvider,
  Button,
  Box,
  Text,
  Link,
  VStack,
  Input,
  Grid,
  theme,
  List,
  ListItem,
  ListIcon,
  OrderedList,
  UnorderedList,
} from '@chakra-ui/react';
  
function Journals(journals){
	const [ListOfJournals,setListOfJournal] = useState([]);
   	async function getData(){
   		try{
			const url = 'http://127.0.0.1:8000/journal/';
			const response = await fetch(url,{method:'GET'});
			const json = await response.json();
			
			console.log('the response for from API is:');
          	setListOfJournal(json['data'][0]);
          	console.log(ListOfJournals);
	   }catch(error){console.error(error);
	   }finally{}
   	}

	useEffect(() => {
		getData();
 	 }, []);
	

	return (
      <Box textAlign="left" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <VStack spacing={8}>
          	<OrderedList fontSize='3xl'>
          		{ListOfJournals.map((j)=>
          			<ListItem key={j['id']}>
          					<Text>{j['title']}</Text>
          					<Text fontSize='sm'>{j['body']}</Text>
          			</ListItem>)}
  			</OrderedList>
	        </VStack>
        </Grid>
      </Box>
		
	);	
}

export default Journals;