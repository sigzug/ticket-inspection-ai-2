import {Box, Flex, HStack, Link, Spacer, Text} from "@chakra-ui/react";
import {BACKEND} from "../../globals.ts";

export function Nav() {
    return (
        <Box as="nav" bg="blue.600" color="white" px="6" py="3" shadow="sm">
            <Flex align="center">
                <Text fontWeight="bold" fontSize="xl">FY</Text>

                <HStack spacing="6" ml="10" display={{base: "none", md: "flex"}}>
                    <Link href="/">Home</Link>
                    <Link href="/about">About</Link>
                    <Link href="/contact">Contact</Link>
                </HStack>

                <Spacer/>

                <HStack spacing="4">
                    {/* Viktig: bruk full URL til Django, så du ikke havner i SPA-routeren */}
                    <Link href={`${BACKEND}/admin/`} rel="noopener">Admin</Link>
                </HStack>
            </Flex>
        </Box>
    );
}
