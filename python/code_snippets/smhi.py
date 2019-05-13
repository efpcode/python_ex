import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from os.path import exists, abspath
from sys import exit
from geopy import Nominatim
from geopy.exc import GeopyError
from bs4 import BeautifulSoup
from numpy import vstack
from json import JSONDecodeError

# Global variables
url_api = "https://opendata-download-metfcst.smhi.se"
url_doc = "https://opendata.smhi.se/apidocs/metfcst/parameters.html"

# input and checks for input failure address
def address_input(address=None):
    """The function prompts user to enter a Swedish address.

    Parameters
    ----------
    address : str(optional)
        The 'address' parameter is optional and if skipped the user is prompted
        to enter input.

    Returns
    -------
    place : geopy.location.Location(object)
        The 'place' is a geopy object that contains geographical information
        e.g. longitude and latitude etc.

    See Also
    --------
    test_address : For more information regardning exception handling.
    """
    place = test_address(address_check=address)  # Check if input is correct

    # Nags user to death or until location is found
    while not place:
        place = address_input()

    return place


def test_address(address_check=None):
    """The function tries to allocate geograpical information.

    Parameters
    ----------
    address_check : str(optional)
        The 'address' is a string that contains a Swedish city name, postcode
        or other geographical information.


    Returns
    -------
        location : geopy.location.Location(object)
            The 'place' is a geopy object that contains geographical informa-
            tion e.g. longitude and latitude etc.
    Raises
    ------
    AttributeError
        If location is not found.

    GeopyError
        If geopy module encounters error.

    Exception
        If unexpeceted bug/error is encountered.

    """
    # Logic for input
    if address_check == None:
        user_input = input("<<< Please enter an address: city in Sweden ")
    else:
        user_input = address_check

    # using geopy module to create locator object.
    geo_loc = Nominatim(user_agent="my_smhi_app")

    # Make sure location exists.
    try:
        location = geo_loc.geocode(user_input)

    except AttributeError as error:
        message = (
            "The location was not found: {} <--> "
            "None type return. \n{}.".format(location, error))

        print(message)

    except GeopyError as errors:
        print("An unexpected error happenden with geopy:"
              " {}".format(errors))

    except Exception as errors:
        print("Something happenden: {}".format(errors))

    else:
        return location


# Web crawler
def get_smhi_parameters(response):
    """Web crawler function that allocates table information
    from global variable 'url_doc'.

    Parameters
    ----------
    response : requests.models.Response(object)
        The 'response' parameter is a 'connection' between web page/ web api.
        Connection is establish through the requests module.

    Returns
    -------
    column_headers, data : tuple(object)
        The 'column_headers' return  are the th-tags in 'url_doc' variable.
        The 'column_headers'return is a list(object) with string typed items.

        The 'data' are the td-tags in 'url_doc' variable. The 'data' return is
        a nested list(object). The nested structure of the 'data' return is
        visualized in 'Examples'. All the item in the nested 'data' return
        have a length equalt to 6.

    Examples
    --------
    >>> column_headers, data = get_smhi_parameters(response)
    ["A", "B", "C"], [[1,2,3,4,5,6], ["a", "b", "c", "d", "e", "f"]]

    """
    # Local global variables
    column_headers = []
    data = []
    id_name = "pmp3g-parameters"

    # Gets html from smhi doc page
    smhi_soup = BeautifulSoup(response.text, "html.parser")

    # Gets the table with parameter descritions.
    p_table = smhi_soup.find("div", attrs={"id":id_name})

    if p_table == None:
        text = (f"Crawler cannot find element called '{id_name}'. "
                f"Please visit page {url_doc} to update id.")
        raise ValueError(text)

    # Gets/finds only the elements inside tbody tags
    p_tbody = p_table.find("tbody")

    # Gets/finds all tr elements i.e. the rows in parameter table.
    p_rows = p_tbody.find_all("tr")

    # Itering inside rows to find headers and data.

    for row in p_rows:

        # Finds all the table header tags.
        row_headers = row.find_all("th")

        # Iters rows finds table headers and appends to column_headers
        column_headers.append(
            [head.text.strip() for head in row_headers if head])


        # Finds all the table data tags.
        data_row = row.find_all("td")

        # Iters rows finds data in table appends to data.
        data.append(
            [point.text.strip() for point in data_row]
        )

    # Removes empty None Data and checks that data has len of 6
    data = [i for i in data if len(i) == 6]
    column_headers = [i for i in column_headers if i]

    # Closes connection to smhi doc page.
    response.close()

    return (column_headers, data)


def get_parameter_table(column_headers, data):
    """The function creates a csv file and pandas.DataFrame(object)
    from the return values given by get_smhi_parameters function.

    Parameters
    ----------
    column_headers : list(object)
        The 'column_headers' parameter is a list object. The objects is
        populated by th-tags found in variable 'url_doc'. List items consists
        of string elements.

    data : list(object)
        The 'data' parameter is a nested list object. For more information
        about structure see 'Examples' in get_smhi_parameters function.

    Returns
    -------
    df : pandas.core.frame.DataFrame(object)
        The 'df' is a dataframe object. The object function as placeholder
        for the table found in variable 'url_doc'.
        The table consist of key-pair values for the smhi-api.
        The table is limited to the most common weather phenomena.

    file_name : csv-file
        The 'file_name' is not return value. The 'file_name' is a csv-file,
        which contains the values in 'df' returna as a csv-file.
        The 'file_name' is set to 'parameters_smhi' as default.

    See Also
    --------
    test_file_parser : For more information about overwrtining conflict.


    """
    df = pd.DataFrame(vstack(data), columns=column_headers)
    file_name = "parameters_smhi"
    file_name = test_file_parser(file_name)
    df.to_csv(f"./{file_name}.csv", sep=",", index=False)
    print("File was created :{}".format(abspath("./"+file_name+".csv")))
    return df


# Connecting to smhi api.
def smhi_api_get(url, location=None):
    """The function tries connect to either to smhi api (see variable called
    'url_api') or the web doc page (see variable called 'url_doc').

    Parameters
    ----------
    url : str
        The 'url' is a postional argument. The 'url' accepts string typed
        input. See variables 'url_api' and 'url_doc'.

    location : geopy.location.Location(optional)
        The 'location' is an optional argument that is passed to retrieved a 10
        day forecast from the smhi-api.

    Returns
    -------
    response : requests.models.Response(object)
        The 'response' return has two types of values. If 'url_api' is passed
        the response return is json (object). Otherwise the return is plain
        html if 'url_doc' is passed.

    Raises
    ------
    HTTPError
        If 'location' is outbounds.
        If status code 400.

    RequestError
        If other status code is obtain than 400 e.g. TimedOutError, Connection
        etc.

    See Also
    --------
    test_smhi_api_get : For more information about exception handling.
    address_input : For more information about 'location'.

    """

    if location:
    # Calling smhi api.
        url_get = (url + "/api/category/pmp3g/version/2/geotype/point/lon/"
                   "{:0.5f}/lat/{:0.5f}/data.json".format(
                       location.longitude, location.latitude))
    else:
        url_get = url

    response = test_smhi_api_get(url_get)

    return response


def test_smhi_api_get(url):
    """The function tests connection agains web page and smhi api.

    Parameters
    ----------
    url : str
        The 'url' is a string object that points to a webpage or api.
        Two valid values to pass as 'url' are 'url_doc' and 'url_api'.

    Returns
    -------
    response : requests.models.Response(object)
        The 'response' object is return if exception handling is passed.
        The object can either be an html or json object. The 'response' object
        is determine by the variables 'url_doc' and 'url_api'.

    Raises
    ------
    HTTPError
        If 'location' is not found in smhi api or response is 400.

    RequestException
        If other status codes are raised by the raise_for_status() function.

    See Also
    --------
    test_smhi_api_get : For more information about exception handling.
    address_input : For more information about 'location'.

    """
    response = requests.get(url, timeout=3.0)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(">>> Location not found, please enter a swedish city:\n {}".format(error))
        address_input()
    except requests.exceptions.RequestException as errors:
        print(">>> The smhi api encounterd a problem:\n{}".format(errors))
        exit(1)
    else:
        return response


# Creation of local files
def file_parser_api(response, file_name="smhi"):
    """The function only accepts requests.get from 'url_api' variable.
    The function gets a 10 day forecast and stores it as a csv-file.

    Parameters
    ----------
    response : requests.models.Response(object)
        The 'response' parameter is tied to the request made to smhi api.
        The function accepts requests made with 'url_api' variable.

    file_name : str(optional)
        The 'file_name' parameter is the name of the csv-file created.
        Default value is set to 'smhi'.

    Returns
    -------
    file_name : str(object)
        The 'file_name' is the return value of the function. The 'file_name'
        is later used for sampling and filtering of data.

    Raises
    ------
    JSONDecodeError
        If 'response' object is not json object.

    Exception
        If unexpected error/bug occurs.

    """

    # Trying to create a json object
    try:
        todo = response.json()
    except JSONDecodeError as error:
        print(f"Get request only valid for json object:\n"
              f"{response} --> invalid json: {error} ")
        return
    except Exception as errors:
        print("Unexpected error occurred, shutting down:\n {errors}")
        return

    # Test if file exits in file-system
    file_name = test_file_parser(file_name, suffix=".csv")

    # Creates file and iter over elements in json object.
    with open(f"{file_name}.csv", "w") as f:
        f.write("Composite_Dates"+","+"Name"+"," "Unit" + "," + "Values,\n")
        for data in todo.get("timeSeries"):
            for point in data.get("parameters"):
                f.write("{0},{1},{2},{3},\n".format(
                    data.get("validTime").strip("Z"),
                    point.get("name"),
                    point.get("unit"),
                    str(point.get("values")).strip("[]")
                ))
        f.close()

    # Closing connection to api
    response.close()

    # Prompt to user.
    print(f"{file_name}.csv was created")
    return file_name


def test_file_parser(file_name, suffix=".csv" ):
    """The function is file name maker test function.

    Parameters
    ----------
    file_name : str
        The 'file_name' parameters is a string object with the filename for
        file.

    suffix : str(optional)
        The 'suffix' determines file type. The 'suffix' is the filetype-
        flag e.g. '.csv' or '.txt'.

    Returns
    -------
    file_name : str
        The 'file_name' return is only passed if file name is unique.

    """
    # Gets csv files in current working directory
    csv_files_present =  exists(file_name + suffix)
    count = 0

    while csv_files_present:
        csv_files_present = exists(file_name+ suffix)
        if csv_files_present:
            print(f">>> Try again file exists: {file_name + suffix}", csv_files_present)
            file_name = input("<<< Enter a new file name for csv-file"
                            ":\n<<< ").rstrip(".csv")
            print(f"\n>>> File creation attempts: {count}")
            count +=1

        elif not csv_files_present:
            return file_name

        # In theory this should never run
        else:
            count +=1
            print(f">>> File naming trials: {count}")
            csv_files_present =  True
    return file_name


# Getting down sampling data.
def data_parser_api(file_name, suffix=".csv" ):
    """The function parses api data from 'url_api' and creates three new
    columns.

    file_name : str
        The 'file_name'is the string object returned from file_parser_api
        function.

    suffix : str(optional)
        The 'suffix' parameter flags for filetyp e.g. '.csv', '.txt' or '.jpg'.

    Returns
    -------
    df : pandas.core.frame.DataFrame(object)
        The 'df' return contains the 10 day forecast from the smhi api.

    See Also
    --------
    file_parser_api : For more information about 'file_name'.

    """
    # Creates abosolute path for file
    find_path = abspath(file_name + suffix)
    df = pd.read_csv(find_path, sep=",", header=0, usecols=range(4))

    # Splits column called "Composite_Dates" into two new columms
    df["Dates"], df["Time"] = df.Composite_Dates.str.split("T").str

    # Creates time and data composite
    df["Date_Time"] = df.Dates + " " + df.Time

    # Creates Series of Dates columns
    s_dates = df.Dates

    df["Weekday"] = pd.to_datetime(s_dates).apply(lambda x: x.day_name())

    return df


def filter_data(df, file_name="smhi_filter", filter_key="t"):
    """The function reduces the 10 day forecast to a weather trait.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame(object)
        The 'df' is the return value from the data_parser_api function.

    file_name : str(optional)
        The 'file_name' is filename for the csv-file created.
        Default value for 'file_name' is 'smhi_filter'.

    filter_key : str(optional)
        The 'filter_key' parameter is string object that filters
        the data in 'df'. The filter is concern to single weather phenomena.

    Returns
    -------
    df_filter, file_name : tuple(pandas.core.frame.DataFrame(object), str)
        The 'df_filter' is the data retrieved from the smhi api.
        The data is reduce to on single weather trait. The 'file_name'
        is the name of the csv-file created.


    csv-file : None
        The 'csv-file' is the 'df_filter' return stored as csv-file.


    """
    df_filter = df[df["Name"]==filter_key]
    file_name = test_file_parser(file_name, suffix=".csv")

    if file_name:
        df_filter.to_csv(f"./{file_name}.csv", sep=",", index=False)
        return (df_filter, file_name)
    else:
        print(f">>> File was not created: {file_name + suffix}")
        return
    return f"File was created {file_name + suffix}"


# Plotting data

def plot_line(file_name, location, parameter, suffix=".csv"):
    """The function creates a line figure. The figure is saved as png and
    has the aspect 16 X 8 inches.

    Parameters
    ----------
    file_name : str
        The 'file_name' parameter is the name of the file that has been
        filtered with filter_data function.

    location : geopy.location.Location(object)
        The 'location' object contains geographic information about the
        data retrieved from the smhi api

    parameters : pandas.core.frame.DataFrame(object1)
        The 'parameter' is the table retrieved with the 'url_doc' request.


    suffix : str(optional)
        The 'suffix' is the filetype flag e.g. .csv, .jpg or png.

    Returns
    -------
    png : file(object)
        The 'png' created from the 'file_name' file.
    """
    # Creates path to file.
    file_name = file_name.rstrip(".csv")
    find_path = abspath(file_name+suffix)

    # Reads down filter data.
    data = pd.read_csv(
        find_path, sep =",", header=0, parse_dates=["Date_Time"],
        usecols=["Date_Time", "Values"]
    )

    # Calcultes mean values of weather phenomena.
    data["Mean"] = data.Values.mean()

    # Sets YY-mm-dd H:M:S as index for data.
    data.set_index("Date_Time", inplace=True)

    # Changeing art direction.
    if "ggplot" in plt.style.available:
        plt.style.use("ggplot")


    # Creates figure objects
    fig, ax = plt.subplots(figsize=(16,8))

    # Plotting x and y values
    ax.plot(data.index, data.Values,"g-", label=f"{parameter.Unit[0]}", lw=3.5)
    ax.plot(data.index, data.Mean,"k--",label="Mean",lw=1.2)

    # Creating Text object in figure like y-axis label
    plt.title(f"Forecast for the next 10 days in {location.address}")  # Fig title
    ax.set_xlabel("")  # X-axis fig label
    ax.set_ylabel(f"{parameter.Description[0]}")  # Y-axis label
    # Legend of data points and removes frame around it
    ax.legend(frameon=False)

    # X-axis formatting
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))  # Minor ticks hours
    plt.minorticks_on()  # Plotting minor ticks in figure.

    # Lowering Major ticks of x-axis.
    plt.tick_params(axis="x", which="major", pad=10.8, length=20, width=2.1)

    # Saving figure as png file
    fig.savefig(file_name+".png")

    # Closing all figure object open.
    plt.close("all")

    return f"File created {file_name}"


# User choices

def user_choice(t_parameters):
    """The function creates opportunity to choose a weather trait.

    Parameters
    ----------
    t_parameters : pandas.core.frame.DataFrame(object)
        The is the table from the get request with 'url_doc'.

    Returns
    -------
    df : pandas.core.frame.DataFrame(object)
        The 'df' contains all the descriptions and units for a certain
        weather trait

    Raises
    ------
    ValueError
        If input not converted to integer.
    KeyError
        If input cannot slice 't_parameters' object.

    See Also
    --------
    test_user_input : For more information about exception handling.
    """


    user_input = None  # Makes while loop falsifiable
    choice = dict(zip(t_parameters.index, t_parameters.Description.unstack()))

    for k, v in choice.items():
        print("{} <---> {}\n".format(k,v))

    while not user_input:
        user_input = test_user_input(t_parameters)

    df = t_parameters.loc[user_input]

    return df


def test_user_input(t_parameters):
    """The function tries to catch invalid user input.

    Parameters
    ----------
    t_parameters : pandas.core.frame.DataFrame(object)
        The is the table from the get request with 'url_doc'.

    Returns
    -------
    answer : int(object)
        The 'answer' is a valid index in the 't_parameters' object.

    Raises
    ------
    ValueError
        If 'answer' cannot be converted to an integer.
    KeyError
        If 'answer' incapable of slicing 't_parameters' with loc function.

    """
    try:
        answer = int(input(">>> Enter the an index number: "))
        t_parameters.loc[answer]

    except ValueError as error:
        print("Not a valid digit {}".format(error))

    except (KeyError, TypeError) as error2:
        print("Index not found in {0}\n{1}.".format(t_parameters.index, error))
    except Exception as errors:
        print(f"Unexpected error happend:\n {errors}")
    else:
        return answer


# Recipe functions
def smhi_web_crawler(url_doc):
    """The function retrieves data from 'url_doc' variable.

    Parameters
    ----------
    url_doc : str
        The 'url_doc' is a string object that enables connection to
        smhi documention regarding data structure.

    Returns
    -------
    smhi_descript : pandas.core.frame.DataFrame(object)
        The 'smhi_descript' is an object that contains parsed
        information about the data obtained through the smhi api.

    See Also
    --------
    smhi_api_get : For more information regarding 'location' variable.
    get_smhi_parameters : For more information about parsing web data.
    get_parameter_table : For more information about 'smhi_descript'


    """

    # Establish connection to smhi doc_page.
    smhi_doc_request = smhi_api_get(url_doc, location=None)

    # Parsing data docpage of smhi.
    columns, data = get_smhi_parameters(smhi_doc_request)

    # Creating file and DataFrame object of web content.
    smhi_descript = get_parameter_table(columns, data)

    # Fixing minor issue with table
    smhi_descript.iat[18, 0] = "Wsymb2"

    return smhi_descript


def smhi_forecast(url_api, choice):
    """The function is recipe that fetches data from the smhi api.
    The function must pass the 'url_api' as well as the 'choice' parameters
    to work properly.

    Parameters
    ----------
    url_api : str
        The 'url_api' is the entry point to the smhi api.

    choice : pandas.core.frame.DataFrame(object)
        The 'choice' is the return object from user_choice function.

    Returns
    -------
    smhi_sample, smhi_sample_name, location : tuple(DataFrame, str, geopy)
        The return is a tuple of length 3. The 'smhi_smaple' is a pd.DataFrame
        object populated with data for a single weather phenomena.

        The 'smhi_sample_name' is str object with the csv-file name for the
        data retrieved in 'smhi_sample'

        The 'location' is the return object from address_input function.
        The object has geographical information.

    files : csv-files
        The function returns csv-files.

    See Also
    --------
    user_choice : For more information about 'choice' parameter.
    address_input : For more information about 'location' return.
    smhi_api_get : For more information about 'smhi_api_request' variable and
                   error handling of connection to api.
    file_parser_api : For more information about 'smhi_forecast_filename'.
    data_parser_api : For more information about 'smhi_data'.
    filter_data : For more information about 'smhi_sample' and
                  'smhi_sample_name' returns.

    Notes
    -----
    For information about errors and other types of exception handling see
    parent/rot functions.

    """
    # Getting geographic information.
    location = address_input()

    # Establish connection to smhi api
    smhi_api_request = smhi_api_get(url_api, location=location)

    # Creating data file from obtained data
    smhi_forecast_filename = file_parser_api(smhi_api_request)

    # Creating pd.DataFrame object
    smhi_data = data_parser_api(smhi_forecast_filename)

    # Sampled Data
    smhi_sample, smhi_sample_name = filter_data(
        smhi_data,
        file_name="weather_sample",
        filter_key=choice.Parameter[0]
    )

    return (smhi_sample, smhi_sample_name, location)


def main():
    """ This function streamlines the calling of different functions.

    Parameters
    None : None
        Nothing is needed.

    Returns
    -------
    files : csv
        The 'files' returned from the function are data extraction from
        either the 'url_api' variable or the 'url_doc' variable.

    file : png
        The 'png' return is a single weather trait plotted as line where
        x-axis is the time dimesion and the y-axis the values of the weather
        phenomena.

    str : str
        The 'str' return is a message of termination of script.
    """
    smhi_data_describe = smhi_web_crawler(url_doc)

    sample_choice = user_choice(smhi_data_describe)

    smhi_sample, smhi_file, geo_loc = smhi_forecast(url_api, sample_choice)

    plot_line(smhi_file, geo_loc, sample_choice)

    return ">>> Finshed!"


if __name__ == "__main__":
    prompt = main()
    print(prompt)





