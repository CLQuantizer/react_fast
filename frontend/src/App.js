import React, {useEffect, useState} from 'react';
import {useFormik,Formik,Field,Form} from 'formik';
import DataTable from './DataTable';
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
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Logo } from './Logo';


function App() {
   // set the title of the page 
	 document.title='Word Relatedness API'

   // define the states
   const [isLoading,setLoading] = useState(true);
   const [data, setData] = useState([]);
   const [target, setTarget] = useState([]);

   // function that converts JSON data into list
   const makeData = (words,probs)=>{
	   let results = [];
	   for(let i=0;i<words.length;i++){
	   	results.push({word:words[i],prob:probs[i]});
	   }
	   return results
   }  

   // function that does POST with target word
   const getList = async (target)=>{
	   try{
		var url = 'http://127.0.0.1:8000/related/'+target;
		const response = await fetch(url,{method:'POST'})
		const json = await response.json();
		var results = makeData(json.words,json.probs);
	        setData(results);
          console.log('the response for \''+ target +'\' from API is:');
          console.log(results);
	   }catch(error){console.error(error);
	   }finally{
      console.log('generating the DataTable')
		  setLoading(false);
	   }
	}

    // react hook
    useEffect(() => {
      if(target==''){setTarget('whatever');
      console.log('initial rendering, setting the word to \'whatever\'')}
      else{getList(target);console.log('the word has been set to: '+target)}
 	 }, [target]);
   
   // another component?
   const SearchForm=()=>{
        const formik = useFormik({
          initialValues:{word: target,},
		      onSubmit:(values,actions)=>{
      			actions.setSubmitting(false);
      			setTarget(values.word);
      			console.log('now submitting the word: '+values.word);
	         },
    });
        return(
        <form onSubmit = {formik.handleSubmit}>
         <label htmlFor='word'>Enter a word to search for its 15 most related words<br/></label>
         <Input id ='word'
            name = 'word'
            type = 'word'
            width = 'auto'
            onChange = {formik.handleChange}
            value = {formik.values.word}
        />
        <Button type="submit">Search</Button>
        </form>
        );
    };

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <VStack spacing={8}>
            <Logo h="15vmin" pointerEvents="none" /> 
              <SearchForm/>
    	        <DataTable data={data}/>
	        </VStack>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
