import { 
  ChakraProvider,
  Button,
  Box,
  Link,
  Grid,
  GridItem,
  theme,
} from '@chakra-ui/react';
import React, {StrictMode, useEffect, useState} from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter,Routes,Route,} from "react-router-dom";

import App from './App';
import MyPage from './MyPage';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import Journals from './Journals'
import Config from './Config';

const serverUrl = Config.server;

function Index(){
      const [accessToken, setAccessToken] = useState('');
      const [expiration, setExpiration] = useState(0);
      const [isLoggedIn, setIsLoggedIn] = useState(false);

  // useEffect(()=>{
  //   function good(){
  //     setAccessToken(localStorage.getItem('accessToken'));
  //     setExpiration(localStorage.getItem('expiration'));

  //     console.log('index isLoggedIn: '+isLoggedIn);
  //     console.log('index 1');
  //   }
  //   return function cleanup(){good();console.log('index 1 cleanup');}
  // }
  // ,);

  return (
  <StrictMode>
  <ChakraProvider theme={theme}>
  <Box textAlign="center" fontSize="xl">
    <Grid minH="5vh" p={3}>
      <ColorModeSwitcher justifySelf="flex-end" />
    </Grid>

    <Grid templateColumns='repeat(3, 1fr)' gap={6}>
      <GridItem w='100%' h='10' >
        <Button variant = 'outline'>
          <Link href ={serverUrl}>Home</Link>
        </Button>
      </GridItem>

      <GridItem w='100%' h='10'>
        <Button variant = 'outline'>
          <Link href = {serverUrl +'journals/'}>Journals</Link>
        </Button>
      </GridItem>

      <GridItem w='100%' h='10'>
        <Button variant = 'outline'>
          {/* <Link href ={serverUrl+'login/'}>{isLoggedIn===true ? 'Login':'logout' }</Link> */}
          <Link href ={serverUrl+'login/'}>Login</Link>
        </Button>
      </GridItem>

    </Grid>
  </Box>
  <br/>
    <BrowserRouter>
    <Routes>
      <Route path = "" element={<App/>}/>
      <Route path = "journals/" element={<Journals/>}/>
      <Route path = "login/" element={<MyPage 
          accessToken={accessToken}
          isLoggedIn={isLoggedIn}
          expiration={expiration}
          setAccessToken={setAccessToken} 
          setIsLoggedIn={setIsLoggedIn}
          setExpiration={setExpiration}
        />}
      />
    </Routes>
    </BrowserRouter>
  </ChakraProvider>  
</StrictMode>);
}

ReactDOM.render(<Index/>, document.getElementById('root'));

