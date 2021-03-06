module Defendant exposing (Defendant, decoder)

import Json.Decode as Decode exposing (Decoder, int, nullable, string)
import Json.Decode.Pipeline exposing (required)


type alias VerifiedPhone =
    { callerName : Maybe String
    , phoneType : Maybe String
    , nationalFormat : String
    }


type alias Defendant =
    { id : Int
    , name : String
    , firstName : String
    , middleName : Maybe String
    , lastName : String
    , suffix : Maybe String
    , address : String
    , potentialPhones : Maybe String
    , verifiedPhone : Maybe VerifiedPhone
    }


verifiedPhoneDecoder : Decoder VerifiedPhone
verifiedPhoneDecoder =
    Decode.succeed VerifiedPhone
        |> required "caller_name" (nullable string)
        |> required "phone_type" (nullable string)
        |> required "national_format" string


decoder : Decoder Defendant
decoder =
    Decode.succeed Defendant
        |> required "id" int
        |> required "name" string
        |> required "first_name" string
        |> required "middle_name" (nullable string)
        |> required "last_name" string
        |> required "suffix" (nullable string)
        |> required "address" string
        |> required "potential_phones" (nullable string)
        |> required "verified_phone" (nullable verifiedPhoneDecoder)
