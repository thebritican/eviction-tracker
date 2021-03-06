module Page.WarrantHelp exposing (Model, Msg, init, subscriptions, toSession, update, view)

import Api exposing (Cred)
import Api.Endpoint as Endpoint
import Date
import Defendant exposing (Defendant)
import DetainerWarrant exposing (DetainerWarrant)
import Element exposing (Element, fill)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Element.Input
import Html exposing (Html)
import Html.Events
import Http
import Json.Decode as Decode
import Palette
import Session exposing (Session)
import User exposing (User)


type alias Model =
    { session : Session
    , warrants : List DetainerWarrant
    , query : String
    , warrantsCursor : Maybe String
    }


getWarrants : Maybe Cred -> Cmd Msg
getWarrants viewer =
    Api.get Endpoint.detainerWarrants viewer GotWarrants Api.detainerWarrantApiDecoder


init : Session -> ( Model, Cmd Msg )
init session =
    let
        maybeCred =
            Session.cred session
    in
    ( { session = session
      , warrants = []
      , query = ""
      , warrantsCursor = Nothing
      }
    , getWarrants maybeCred
    )


type Msg
    = InputQuery String
    | SearchWarrants
    | GotWarrants (Result Http.Error (Api.Collection DetainerWarrant))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputQuery query ->
            ( { model | query = query }, Cmd.none )

        SearchWarrants ->
            let
                maybeCred =
                    Session.cred model.session
            in
            ( model, getWarrants maybeCred )

        GotWarrants result ->
            case result of
                Ok detainerWarrantsPage ->
                    ( { model | warrants = detainerWarrantsPage.data, warrantsCursor = detainerWarrantsPage.meta.afterCursor }, Cmd.none )

                Err errMsg ->
                    ( model, Cmd.none )


view : Maybe User -> Model -> { title : String, content : Element Msg }
view profile model =
    { title = "Warrant Help"
    , content =
        Element.row [ Element.centerX, Element.padding 10, Font.size 20, Element.width (fill |> Element.maximum 1000 |> Element.minimum 400) ]
            [ Element.column [ Element.centerX, Element.spacing 10 ]
                ((case profile of
                    Just user ->
                        [ Element.row [ Element.centerX, Font.center ] [ Element.text ("Hello " ++ user.firstName ++ ", one of these may be your detainer warrant: ") ] ]

                    Nothing ->
                        []
                 )
                    ++ [ Element.row [ Element.centerX, Element.width (fill |> Element.maximum 1000 |> Element.minimum 400) ]
                            (if List.isEmpty model.warrants then
                                []

                             else
                                [ viewWarrants model ]
                            )
                       ]
                )
            ]
    }


viewDefendant : Defendant -> Element Msg
viewDefendant defendant =
    viewTextRow defendant.name


viewDefendants : DetainerWarrant -> Element Msg
viewDefendants warrant =
    Element.column []
        (List.map viewDefendant warrant.defendants)


viewTextRow text =
    Element.row
        [ Element.width fill
        , Element.padding 10
        , Border.solid
        , Border.color Palette.grayLight
        , Border.widthEach { bottom = 1, left = 0, right = 0, top = 0 }
        ]
        [ Element.text text ]


viewHeaderCell text =
    Element.row
        [ Element.width fill
        , Element.padding 10
        , Font.semiBold
        , Border.solid
        , Border.color Palette.grayLight
        , Border.widthEach { bottom = 1, left = 0, right = 0, top = 0 }
        ]
        [ Element.text text ]


viewWarrants : Model -> Element Msg
viewWarrants model =
    Element.table [ Font.size 14 ]
        { data = List.filter (\warrant -> List.any (\defendant -> String.contains (String.toUpper model.query) (String.toUpper defendant.name)) warrant.defendants) model.warrants
        , columns =
            [ { header = viewHeaderCell "Docket ID"
              , width = fill
              , view =
                    \warrant ->
                        viewTextRow warrant.docketId
              }
            , { header = viewHeaderCell "Court Date"
              , width = fill
              , view = viewTextRow << Maybe.withDefault "" << Maybe.map Date.toIsoString << .courtDate
              }
            , { header = viewHeaderCell "File Date"
              , width = fill
              , view = viewTextRow << Date.toIsoString << .fileDate
              }
            , { header = viewHeaderCell "Defendants"
              , width = fill
              , view = viewDefendants
              }
            , { header = viewHeaderCell "Plaintiff"
              , width = fill
              , view =
                    viewTextRow << Maybe.withDefault "" << Maybe.map .name << .plaintiff
              }
            ]
        }


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- EXPORT


toSession : Model -> Session
toSession model =
    model.session
