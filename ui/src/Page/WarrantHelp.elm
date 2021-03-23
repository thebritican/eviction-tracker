module Page.WarrantHelp exposing (Model, Msg, init, subscriptions, toSession, update, view)

import Api
import DetainerWarrant exposing (Defendant, DetainerWarrant)
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


type alias Model =
    { session : Session
    , warrants : List DetainerWarrant
    , query : String
    , warrantsCursor : Maybe String
    }


getWarrants : String -> Cmd Msg
getWarrants query =
    Http.get
        { url = "/api/v1/detainer-warrants/?defendant_name=" ++ query
        , expect = Http.expectJson GotWarrants Api.detainerWarrantApiDecoder
        }


init : Session -> ( Model, Cmd Msg )
init session =
    ( { session = session
      , warrants = []
      , query = ""
      , warrantsCursor = Nothing
      }
    , Cmd.none
    )


type Msg
    = InputQuery String
    | SearchWarrants
    | GotWarrants (Result Http.Error (Api.ApiPage DetainerWarrant))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputQuery query ->
            ( { model | query = query }, Cmd.none )

        SearchWarrants ->
            ( model, getWarrants model.query )

        GotWarrants result ->
            case result of
                Ok detainerWarrantsPage ->
                    ( { model | warrants = detainerWarrantsPage.data, warrantsCursor = detainerWarrantsPage.meta.afterCursor }, Cmd.none )

                Err errMsg ->
                    ( model, Cmd.none )


view : Model -> { title : String, content : Element Msg }
view model =
    { title = "Warrant Help"
    , content =
        Element.row [ Element.centerX, Element.padding 10, Font.size 20, Element.width (fill |> Element.maximum 1000 |> Element.minimum 400) ]
            [ Element.column [ Element.centerX ]
                [ Element.row [ Element.centerX, Font.center ] [ Element.text "Find your Detainer Warrant case" ]
                , viewSearchBar model
                , Element.row [ Element.centerX, Element.width (fill |> Element.maximum 1000 |> Element.minimum 400) ]
                    (if List.isEmpty model.warrants then
                        []

                     else
                        [ viewWarrants model ]
                    )
                ]
            ]
    }


viewDefendant : Defendant -> Element Msg
viewDefendant defendant =
    viewTextRow defendant.name


viewDefendants : DetainerWarrant -> Element Msg
viewDefendants warrant =
    Element.column []
        (List.map viewDefendant warrant.defendants)


viewCourtDate : DetainerWarrant -> Element Msg
viewCourtDate warrant =
    viewTextRow
        (case warrant.courtDate of
            Just courtDate ->
                courtDate

            Nothing ->
                "Unknown"
        )


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
              , view = viewCourtDate
              }
            , { header = viewHeaderCell "File Date"
              , width = fill
              , view =
                    \warrant ->
                        viewTextRow warrant.fileDate
              }
            , { header = viewHeaderCell "Defendants"
              , width = fill
              , view = viewDefendants
              }
            , { header = viewHeaderCell "Plantiff"
              , width = fill
              , view =
                    \warrant ->
                        viewTextRow warrant.plantiff.name
              }
            ]
        }


onEnter : msg -> Element.Attribute msg
onEnter msg =
    Element.htmlAttribute
        (Html.Events.on "keyup"
            (Decode.field "key" Decode.string
                |> Decode.andThen
                    (\key ->
                        if key == "Enter" then
                            Decode.succeed msg

                        else
                            Decode.fail "Not the enter key"
                    )
            )
        )


viewSearchBar : Model -> Element Msg
viewSearchBar model =
    Element.row
        [ --Element.width fill
          Element.spacing 10
        , Element.padding 10
        , Element.centerY
        , Element.centerX
        ]
        [ Element.Input.search
            [ Element.width (fill |> Element.maximum 600)
            , onEnter SearchWarrants
            ]
            { onChange = InputQuery
            , text = model.query
            , placeholder = Just (Element.Input.placeholder [] (Element.text "Search for a defendant"))
            , label = Element.Input.labelHidden "Search for a defendant"
            }
        , Element.Input.button
            [ Element.centerY
            , Background.color Palette.redLight
            , Element.focused [ Background.color Palette.red ]
            , Element.height fill
            , Font.color (Element.rgb 255 255 255)
            , Element.padding 10
            , Border.rounded 5
            ]
            { onPress = Just SearchWarrants, label = Element.text "Search" }
        ]


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- EXPORT


toSession : Model -> Session
toSession model =
    model.session