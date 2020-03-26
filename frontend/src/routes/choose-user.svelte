<script>
    let users = [
        {id: '1', name: 'Lev Chelyadinov'},
        {id: '2', name: 'Natalia Matrosova'},
        {id: '3', name: 'Vladislav Kantaev'},
        {id: '4', name: 'Marina Ivanova'},
        {id: '5', name: 'Alexandr Grichshenko'},
    ]
</script>

<div>
        <p id = "textp">Choose user to enter the service:<p>
        <p><select name="Student">
            <option disabled selected>--Choose User--</option>
            {#each users as user}
            <option id={user.id}>{user.name}</option>
            {/each}
        </select></p>
        <div>
            <a href="http://10.90.138.82/">
            <input type="submit" value="Continue">
            </a>
        </div>
</div>

<style>
    div{
    font-family: Electrica, sans-serif;
    }

    #textp{
        font-weight: bold;
        font-size: 25px;
    }
    select{
        background-color: rgb(222, 222, 222);
        padding: 8px 8px 8px 8px;
        font-family: Electrica, sans-serif;
        border-width: 1.5px;
        border-color: violet;
        border-radius: 10px;
    }

    input{
        padding: 8px 8px 8px 8px;
        font-family: Electrica, sans-serif;
        border-width: 1.5px;
        border-color: violet;
        border-radius: 10px;
    }
</style>
